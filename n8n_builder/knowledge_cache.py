"""
Enhanced Knowledge Cache for MCP Research Tool

This module provides sophisticated caching capabilities for research results,
including persistent storage, cache invalidation, and performance optimization.
"""

import json
import time
import hashlib
import pickle
import logging
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import threading

logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    """Represents a cached research result."""
    key: str
    data: Any
    timestamp: float
    ttl: int
    access_count: int = 0
    last_accessed: float = 0.0
    size_bytes: int = 0
    source: str = "unknown"
    
    def is_expired(self) -> bool:
        """Check if the cache entry has expired."""
        return (time.time() - self.timestamp) > self.ttl
    
    def is_stale(self, staleness_threshold: int = 1800) -> bool:
        """Check if the cache entry is stale (older than threshold)."""
        return (time.time() - self.timestamp) > staleness_threshold
    
    def access(self):
        """Mark the entry as accessed."""
        self.access_count += 1
        self.last_accessed = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'key': self.key,
            'data': self.data,
            'timestamp': self.timestamp,
            'ttl': self.ttl,
            'access_count': self.access_count,
            'last_accessed': self.last_accessed,
            'size_bytes': self.size_bytes,
            'source': self.source
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CacheEntry':
        """Create from dictionary."""
        return cls(**data)

class EnhancedKnowledgeCache:
    """
    Enhanced caching system for research results with persistence and optimization.
    """
    
    def __init__(
        self,
        cache_dir: str = "cache",
        default_ttl: int = 3600,
        max_memory_size: int = 100 * 1024 * 1024,  # 100MB
        max_disk_size: int = 500 * 1024 * 1024,    # 500MB
        cleanup_interval: int = 300,  # 5 minutes
        enable_persistence: bool = True
    ):
        """
        Initialize the enhanced knowledge cache.
        
        Args:
            cache_dir: Directory for persistent cache storage
            default_ttl: Default time-to-live in seconds
            max_memory_size: Maximum memory cache size in bytes
            max_disk_size: Maximum disk cache size in bytes
            cleanup_interval: Cleanup interval in seconds
            enable_persistence: Whether to enable persistent storage
        """
        self.cache_dir = Path(cache_dir)
        self.default_ttl = default_ttl
        self.max_memory_size = max_memory_size
        self.max_disk_size = max_disk_size
        self.cleanup_interval = cleanup_interval
        self.enable_persistence = enable_persistence
        
        # In-memory cache
        self.memory_cache: Dict[str, CacheEntry] = {}
        self.memory_size = 0
        
        # Cache statistics
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'disk_reads': 0,
            'disk_writes': 0,
            'cleanup_runs': 0
        }
        
        # Thread safety
        self.lock = threading.RLock()

        # Shutdown control
        self._shutdown_event = threading.Event()
        self._cleanup_thread = None

        # Initialize cache directory
        if self.enable_persistence:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Knowledge cache initialized with persistence at {self.cache_dir}")
        else:
            logger.info("Knowledge cache initialized (memory-only)")

        # Start cleanup thread
        self._start_cleanup_thread()
    
    def _generate_cache_key(self, method: str, *args, **kwargs) -> str:
        """Generate a unique cache key for method and arguments."""
        # Create a string representation of all arguments
        key_data = f"{method}:{':'.join(str(arg) for arg in args)}"
        if kwargs:
            key_data += f":{':'.join(f'{k}={v}' for k, v in sorted(kwargs.items()))}"
        
        # Hash the key to ensure consistent length and avoid filesystem issues
        return hashlib.sha256(key_data.encode()).hexdigest()[:32]
    
    def _calculate_size(self, data: Any) -> int:
        """Calculate the approximate size of data in bytes."""
        try:
            if isinstance(data, str):
                return len(data.encode('utf-8'))
            elif isinstance(data, (dict, list)):
                return len(json.dumps(data, default=str).encode('utf-8'))
            else:
                return len(pickle.dumps(data))
        except Exception:
            # Fallback estimation
            return len(str(data).encode('utf-8'))
    
    def _get_disk_cache_path(self, key: str) -> Path:
        """Get the disk cache file path for a key."""
        return self.cache_dir / f"{key}.cache"
    
    def _save_to_disk(self, entry: CacheEntry) -> bool:
        """Save cache entry to disk."""
        if not self.enable_persistence:
            return False
        
        try:
            cache_file = self._get_disk_cache_path(entry.key)
            with open(cache_file, 'wb') as f:
                pickle.dump(entry.to_dict(), f)
            
            self.stats['disk_writes'] += 1
            logger.debug(f"Saved cache entry to disk: {entry.key}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to save cache entry to disk: {e}")
            return False
    
    def _load_from_disk(self, key: str) -> Optional[CacheEntry]:
        """Load cache entry from disk."""
        if not self.enable_persistence:
            return None
        
        try:
            cache_file = self._get_disk_cache_path(key)
            if not cache_file.exists():
                return None
            
            with open(cache_file, 'rb') as f:
                entry_data = pickle.load(f)
            
            entry = CacheEntry.from_dict(entry_data)
            
            # Check if entry is expired
            if entry.is_expired():
                cache_file.unlink(missing_ok=True)
                return None
            
            self.stats['disk_reads'] += 1
            logger.debug(f"Loaded cache entry from disk: {key}")
            return entry
        
        except Exception as e:
            logger.error(f"Failed to load cache entry from disk: {e}")
            return None
    
    def _evict_memory_cache(self, target_size: Optional[int] = None):
        """Evict entries from memory cache to free space."""
        if target_size is None:
            target_size = self.max_memory_size // 2  # Evict to 50% capacity
        
        # Sort entries by access frequency and recency (LFU + LRU)
        entries = list(self.memory_cache.values())
        entries.sort(key=lambda e: (e.access_count, e.last_accessed))
        
        evicted_count = 0
        for entry in entries:
            if self.memory_size <= target_size:
                break
            
            # Save to disk before evicting
            if self.enable_persistence:
                self._save_to_disk(entry)
            
            # Remove from memory
            del self.memory_cache[entry.key]
            self.memory_size -= entry.size_bytes
            evicted_count += 1
        
        self.stats['evictions'] += evicted_count
        logger.debug(f"Evicted {evicted_count} entries from memory cache")
    
    def put(self, method: str, data: Any, *args, ttl: Optional[int] = None, source: str = "unknown", **kwargs) -> str:
        """
        Store data in cache.

        Args:
            method: Method name for cache key generation
            data: Data to cache
            *args: Arguments for cache key generation
            ttl: Time-to-live in seconds
            source: Source of the data
            **kwargs: Additional arguments for cache key generation

        Returns:
            Cache key
        """
        with self.lock:
            key = self._generate_cache_key(method, *args, **kwargs)
            ttl = ttl or self.default_ttl
            size = self._calculate_size(data)
            
            entry = CacheEntry(
                key=key,
                data=data,
                timestamp=time.time(),
                ttl=ttl,
                size_bytes=size,
                source=source
            )
            
            # Check if we need to evict memory cache
            if self.memory_size + size > self.max_memory_size:
                self._evict_memory_cache()
            
            # Store in memory cache
            self.memory_cache[key] = entry
            self.memory_size += size
            
            # Save to disk if persistence is enabled
            if self.enable_persistence:
                self._save_to_disk(entry)
            
            logger.debug(f"Cached data for key: {key} (size: {size} bytes, ttl: {ttl}s)")
            return key
    
    def get(self, method: str, *args, **kwargs) -> Optional[Any]:
        """
        Retrieve data from cache.
        
        Args:
            method: Method name for cache key generation
            *args, **kwargs: Arguments for cache key generation
            
        Returns:
            Cached data or None if not found/expired
        """
        with self.lock:
            key = self._generate_cache_key(method, *args, **kwargs)
            
            # Check memory cache first
            if key in self.memory_cache:
                entry = self.memory_cache[key]
                
                if entry.is_expired():
                    # Remove expired entry
                    del self.memory_cache[key]
                    self.memory_size -= entry.size_bytes
                    
                    # Remove from disk too
                    if self.enable_persistence:
                        cache_file = self._get_disk_cache_path(key)
                        cache_file.unlink(missing_ok=True)
                    
                    self.stats['misses'] += 1
                    return None
                
                # Update access statistics
                entry.access()
                self.stats['hits'] += 1
                logger.debug(f"Cache hit (memory): {key}")
                return entry.data
            
            # Check disk cache
            if self.enable_persistence:
                entry = self._load_from_disk(key)
                if entry:
                    # Load back into memory cache
                    if self.memory_size + entry.size_bytes > self.max_memory_size:
                        self._evict_memory_cache()
                    
                    entry.access()
                    self.memory_cache[key] = entry
                    self.memory_size += entry.size_bytes
                    
                    self.stats['hits'] += 1
                    logger.debug(f"Cache hit (disk): {key}")
                    return entry.data
            
            self.stats['misses'] += 1
            return None
    
    def invalidate(self, method: str, *args, **kwargs) -> bool:
        """
        Invalidate a specific cache entry.
        
        Args:
            method: Method name for cache key generation
            *args, **kwargs: Arguments for cache key generation
            
        Returns:
            True if entry was found and removed
        """
        with self.lock:
            key = self._generate_cache_key(method, *args, **kwargs)
            
            # Remove from memory
            removed = False
            if key in self.memory_cache:
                entry = self.memory_cache[key]
                del self.memory_cache[key]
                self.memory_size -= entry.size_bytes
                removed = True
            
            # Remove from disk
            if self.enable_persistence:
                cache_file = self._get_disk_cache_path(key)
                if cache_file.exists():
                    cache_file.unlink()
                    removed = True
            
            if removed:
                logger.debug(f"Invalidated cache entry: {key}")
            
            return removed
    
    def clear(self):
        """Clear all cache entries."""
        with self.lock:
            # Clear memory cache
            self.memory_cache.clear()
            self.memory_size = 0
            
            # Clear disk cache
            if self.enable_persistence and self.cache_dir.exists():
                for cache_file in self.cache_dir.glob("*.cache"):
                    cache_file.unlink(missing_ok=True)
            
            logger.info("Cache cleared")
    
    def cleanup(self):
        """Clean up expired entries and optimize cache."""
        if self._shutdown_event.is_set():
            return  # Don't cleanup during shutdown

        with self.lock:
            current_time = time.time()
            expired_keys = []

            # Find expired entries in memory
            for key, entry in self.memory_cache.items():
                if entry.is_expired():
                    expired_keys.append(key)

            # Remove expired entries from memory
            for key in expired_keys:
                entry = self.memory_cache[key]
                del self.memory_cache[key]
                self.memory_size -= entry.size_bytes
            
            # Clean up disk cache
            if self.enable_persistence and self.cache_dir.exists():
                for cache_file in self.cache_dir.glob("*.cache"):
                    try:
                        # Check if file is old enough to be potentially expired
                        file_mtime = cache_file.stat().st_mtime
                        # Ensure file_mtime is a float (sometimes it can be a string)
                        if isinstance(file_mtime, str):
                            try:
                                file_mtime = float(file_mtime)
                            except (ValueError, TypeError):
                                # If conversion fails, use current time to force cleanup check
                                file_mtime = current_time

                        if (current_time - file_mtime) > self.default_ttl:
                            # Try to load and check expiration
                            entry = self._load_from_disk(cache_file.stem)
                            if entry is None:  # Will be None if expired
                                cache_file.unlink(missing_ok=True)
                    except Exception as e:
                        logger.warning(f"Error during cache cleanup for {cache_file}: {e}")
            
            self.stats['cleanup_runs'] += 1
            logger.debug(f"Cache cleanup completed, removed {len(expired_keys)} expired entries")
    
    def _start_cleanup_thread(self):
        """Start background cleanup thread."""
        def cleanup_worker():
            while not self._shutdown_event.is_set():
                # Use wait instead of sleep to allow for immediate shutdown
                if self._shutdown_event.wait(timeout=self.cleanup_interval):
                    break  # Shutdown event was set

                try:
                    if not self._shutdown_event.is_set():
                        self.cleanup()
                except Exception as e:
                    if not self._shutdown_event.is_set():
                        logger.error(f"Error in cache cleanup thread: {e}")

            logger.debug("Cache cleanup thread shutting down")

        self._cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        self._cleanup_thread.start()
        logger.debug("Cache cleanup thread started")

    def shutdown(self):
        """Shutdown the cache system and cleanup threads."""
        logger.info("Shutting down knowledge cache...")

        # Signal shutdown to cleanup thread
        self._shutdown_event.set()

        # Wait for cleanup thread to finish (with timeout)
        if self._cleanup_thread and self._cleanup_thread.is_alive():
            self._cleanup_thread.join(timeout=5.0)
            if self._cleanup_thread.is_alive():
                logger.warning("Cleanup thread did not shutdown gracefully within timeout")

        logger.info("Knowledge cache shutdown complete")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.lock:
            total_requests = self.stats['hits'] + self.stats['misses']
            hit_rate = self.stats['hits'] / total_requests if total_requests > 0 else 0
            
            return {
                'memory_entries': len(self.memory_cache),
                'memory_size_bytes': self.memory_size,
                'memory_size_mb': self.memory_size / (1024 * 1024),
                'hit_rate': hit_rate,
                'total_requests': total_requests,
                **self.stats
            }
