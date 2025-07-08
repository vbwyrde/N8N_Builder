import asyncio
import uvicorn
import os
import sys
import psutil
import logging
import signal
import subprocess
import time
from typing import List, Optional, Any

def is_n8n_builder_process(proc):
    """Identify if a process belongs to N8N Builder specifically."""
    try:
        cmdline = proc.info.get('cmdline', [])
        if not cmdline:
            return False

        cmdline_str = ' '.join(cmdline).lower()

        # Check for specific N8N Builder patterns
        n8n_patterns = [
            'run.py',                    # Our main script
            'run_public.py',             # Public version script
            'n8n_builder.app:app',       # Our FastAPI app
            'n8n_builder',               # Our module name
        ]

        return any(pattern in cmdline_str for pattern in n8n_patterns)

    except Exception:
        return False

def is_current_process_safe(proc, current_pid):
    """Safely detect if this is the current process, handling venv resolution issues."""
    try:
        # Method 1: Direct PID comparison
        if proc.pid == current_pid:
            return True

        # Method 2: Executable path + script comparison (for venv resolution issues)
        current_exe = os.path.abspath(sys.executable)
        try:
            proc_exe = os.path.abspath(proc.exe())
            if proc_exe == current_exe:
                # Same executable, check if it's running the same script
                cmdline = proc.info.get('cmdline', [])
                if len(cmdline) >= 2 and len(sys.argv) >= 1:
                    current_script = os.path.abspath(sys.argv[0])
                    proc_script = os.path.abspath(cmdline[-1])
                    if proc_script == current_script:
                        return True
        except:
            pass

        return False
    except:
        return False

def run_emergency_shutdown():
    """
    Precise emergency shutdown - kill only confirmed N8N Builder processes except current one.
    This prevents port conflicts and hanging processes.
    """
    try:
        current_pid = os.getpid()
        print(f"Running emergency shutdown to ensure clean system state...")
        print(f"Current process PID: {current_pid}")

        # Target ports used by N8N Builder system (removed Enterprise Module port 8081)
        target_ports = [8002, 8003]
        processes_killed = 0

        # Kill processes by port (skip system processes)
        for port in target_ports:
            try:
                for proc in psutil.process_iter(['pid', 'name', 'connections']):
                    try:
                        # Skip system processes (PID 0, 4, etc.)
                        if proc.info['pid'] in [0, 4]:
                            continue

                        connections = proc.info['connections']
                        if connections:
                            for conn in connections:
                                if hasattr(conn, 'laddr') and conn.laddr and conn.laddr.port == port:
                                    print(f"[INFO] Killing process {proc.info['name']} (PID: {proc.info['pid']}) on port {port}")
                                    proc.kill()
                                    processes_killed += 1
                                    break
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
            except Exception as e:
                print(f"[WARNING] Error checking port {port}: {e}")
                continue

        # Kill processes by name pattern (more targeted)
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Skip current process
                if is_current_process_safe(proc, current_pid):
                    continue

                # Check if this is an N8N Builder process
                if is_n8n_builder_process(proc):
                    print(f"[INFO] Killing N8N Builder process: {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.kill()
                    processes_killed += 1

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
            except Exception as e:
                print(f"[WARNING] Error checking process {proc.info.get('name', 'unknown')}: {e}")
                continue

        print(f"Emergency shutdown complete. Killed {processes_killed} processes.")

        # Wait a moment for processes to terminate
        time.sleep(2)

    except Exception as e:
        print(f"[ERROR] Emergency shutdown failed: {e}")

def check_port_available(port: int) -> bool:
    """Check if a port is available for use."""
    try:
        for proc in psutil.process_iter(['pid', 'connections']):
            try:
                connections = proc.info['connections']
                if connections:
                    for conn in connections:
                        if hasattr(conn, 'laddr') and conn.laddr and conn.laddr.port == port:
                            return False
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return True
    except Exception:
        return False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Main function to run the N8N Builder server."""
    
    # Run emergency shutdown to ensure clean state
    run_emergency_shutdown()
    
    # Wait for ports to be released
    await asyncio.sleep(3)
    
    # Verify ports are available
    for port in [8002, 8003]:
        if not check_port_available(port):
            logger.warning(f"Port {port} is still in use after cleanup")
            await asyncio.sleep(1)
            if not check_port_available(port):
                logger.warning(f"Port {port} is still in use after cleanup attempt")

    try:
        # Find an available port starting from 8002
        port = 8002
        max_attempts = 10
        for attempt in range(max_attempts):
            if check_port_available(port):
                break
            port += 1
            if attempt == max_attempts - 1:
                logger.error(f"Could not find an available port after {max_attempts} attempts")
                return

        logger.info(f"Using port {port} for N8N Builder server")

        # Start the FastAPI server
        config = uvicorn.Config(
            "n8n_builder.app:app",
            host="127.0.0.1",
            port=port,
            log_level="info",
            reload=False  # Disable reload to avoid port conflicts
        )
        server = uvicorn.Server(config)

        logger.info(f"Starting N8N Builder server on port {port}...")
        logger.info(f"N8N Builder will be available at: http://localhost:{port}")
        logger.info("🚀 N8N Builder Community Edition - AI-Powered Workflow Generation")

        await server.serve()

    finally:
        logger.info("Starting system shutdown...")

        # Shutdown knowledge cache if available
        try:
            from n8n_builder.knowledge_cache import EnhancedKnowledgeCache
            # Find any active cache instances and shut them down
            import gc
            for obj in gc.get_objects():
                if isinstance(obj, EnhancedKnowledgeCache):
                    obj.shutdown()
            logger.info("Knowledge cache shutdown complete")
        except Exception as e:
            logger.debug(f"Knowledge cache shutdown: {e}")

        logger.info("System shutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    except Exception as e:
        logger.error(f"Error running server: {e}")
        sys.exit(1)
