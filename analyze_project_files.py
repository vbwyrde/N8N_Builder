#!/usr/bin/env python3
"""
N8N Builder Project File Analysis Script

This script analyzes the entire project to:
1. List all files with their sizes and types
2. Identify duplicate files (by content hash)
3. Determine obsolete files based on import/usage analysis
4. Provide cleanup recommendations

Usage: python analyze_project_files.py
"""

import os
import hashlib
import json
import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import datetime

class ProjectAnalyzer:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.files_info = {}
        self.duplicates = defaultdict(list)
        self.imports_map = defaultdict(set)
        self.usage_map = defaultdict(set)
        self.obsolete_files = set()
        
        # Known entry points and important files
        self.entry_points = {
            'run.py',
            'main.py',
            'n8n_builder/app.py',
            'static/index.html',
            'setup.py'
        }
        
        # File patterns to ignore
        self.ignore_patterns = {
            '__pycache__',
            '.git',
            '.pytest_cache',
            'node_modules',
            '.vscode',
            '.idea',
            '*.pyc',
            '*.pyo',
            '*.egg-info'
        }

    def should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored based on patterns."""
        path_str = str(file_path)
        for pattern in self.ignore_patterns:
            if pattern in path_str or file_path.name.startswith('.'):
                return True
        return False

    def get_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return "ERROR"

    def analyze_python_imports(self, file_path: Path) -> Set[str]:
        """Extract imports from Python file."""
        imports = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST to find imports
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.add(node.module)
            except SyntaxError:
                # Fallback to regex for syntax errors
                import_patterns = [
                    r'from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import',
                    r'import\s+([a-zA-Z_][a-zA-Z0-9_.]*)'
                ]
                for pattern in import_patterns:
                    matches = re.findall(pattern, content)
                    imports.update(matches)
                    
        except Exception as e:
            print(f"Error analyzing imports in {file_path}: {e}")
        
        return imports

    def analyze_file_references(self, file_path: Path) -> Set[str]:
        """Find references to other files in the project."""
        references = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for file references
            patterns = [
                r'["\']([^"\']*\.py)["\']',  # Python file references
                r'["\']([^"\']*\.html?)["\']',  # HTML file references
                r'["\']([^"\']*\.js)["\']',  # JavaScript file references
                r'["\']([^"\']*\.css)["\']',  # CSS file references
                r'["\']([^"\']*\.json)["\']',  # JSON file references
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                references.update(matches)
                
        except Exception as e:
            print(f"Error analyzing references in {file_path}: {e}")
        
        return references

    def scan_all_files(self):
        """Scan all files in the project."""
        print("🔍 Scanning all project files...")
        
        for root, dirs, files in os.walk(self.project_root):
            # Remove ignored directories
            dirs[:] = [d for d in dirs if not any(pattern in d for pattern in self.ignore_patterns)]
            
            for file in files:
                file_path = Path(root) / file
                
                if self.should_ignore_file(file_path):
                    continue
                
                try:
                    stat = file_path.stat()
                    file_hash = self.get_file_hash(file_path)
                    
                    relative_path = file_path.relative_to(self.project_root)
                    
                    self.files_info[str(relative_path)] = {
                        'path': file_path,
                        'size': stat.st_size,
                        'modified': datetime.datetime.fromtimestamp(stat.st_mtime),
                        'hash': file_hash,
                        'extension': file_path.suffix,
                        'is_entry_point': str(relative_path) in self.entry_points
                    }
                    
                    # Group by hash for duplicate detection
                    if file_hash != "ERROR":
                        self.duplicates[file_hash].append(str(relative_path))
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        # Build normalized to original path mapping
        self.normalized_to_original = {self.normalize_path(k): k for k in self.files_info.keys()}

    def analyze_dependencies(self):
        """Analyze file dependencies and usage."""
        print("🔗 Analyzing file dependencies...")
        
        for file_path, info in self.files_info.items():
            if info['extension'] == '.py':
                # Analyze Python imports
                imports = self.analyze_python_imports(info['path'])
                self.imports_map[file_path] = imports
                
                # Find references to other project files
                references = self.analyze_file_references(info['path'])
                self.usage_map[file_path] = references
                
                # Mark imported files as used
                for imp in imports:
                    # Convert import to potential file paths
                    potential_files = [
                        f"{imp.replace('.', '/')}.py",
                        f"{imp.replace('.', '/')}" + "/__init__.py",
                        f"n8n_builder/{imp.replace('.', '/')}.py"
                    ]
                    for pot_file in potential_files:
                        if pot_file in self.files_info:
                            self.usage_map[pot_file].add(file_path)

    def find_dynamic_imports(self) -> Set[str]:
        """Scan all Python files for dynamic import patterns and return referenced module/file names."""
        dynamic_imports = set()
        patterns = [
            r"__import__\(['\"]([a-zA-Z0-9_\.]+)['\"]\)",
            r"importlib\.import_module\(['\"]([a-zA-Z0-9_\.]+)['\"]\)",
            r"importlib\.util\.spec_from_file_location\(['\"]([a-zA-Z0-9_\.]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\)",
            r"exec\(open\(['\"]([^'\"]+\.py)['\"]\).read\(\)\)",
            r"runpy\.run_module\(['\"]([a-zA-Z0-9_\.]+)['\"]\)",
            r"runpy\.run_path\(['\"]([^'\"]+\.py)['\"]\)",
        ]
        for file_path, info in self.files_info.items():
            if info['extension'] == '.py':
                try:
                    with open(info['path'], 'r', encoding='utf-8') as f:
                        content = f.read()
                    for pattern in patterns:
                        for match in re.findall(pattern, content):
                            # Some patterns return tuples, some strings
                            if isinstance(match, tuple):
                                for m in match:
                                    if m:
                                        dynamic_imports.add(m)
                            else:
                                dynamic_imports.add(match)
                except Exception as e:
                    print(f"Error scanning for dynamic imports in {file_path}: {e}")
        return dynamic_imports

    def resolve_import_to_path(self, importing_file: str, import_name: str) -> str:
        """Resolve an import (including relative) to a file path in the project."""
        # Handle relative imports (e.g., from .config import config)
        if import_name.startswith('.'):
            # Get the directory of the importing file
            base_dir = str(Path(importing_file).parent)
            # Remove leading dots and join
            rel_import = import_name.lstrip('.')
            if rel_import:
                resolved = os.path.normpath(os.path.join(base_dir, rel_import.replace('.', '/')) + '.py')
            else:
                # 'from . import something' means the __init__.py in the same dir
                resolved = os.path.normpath(os.path.join(base_dir, '__init__.py'))
            return resolved
        # Absolute import
        return import_name.replace('.', '/') + '.py'

    def normalize_path(self, path: str) -> str:
        """Normalize a file path to POSIX style and lower case for comparison."""
        return str(Path(path).as_posix()).lower()

    def identify_obsolete_files(self):
        """Identify files that appear to be obsolete, now including dynamic imports and improved relative import handling."""
        print("🗑️  Identifying obsolete files...")
        
        # Files that are never imported or referenced
        all_files = set(self.normalize_path(f) for f in self.files_info.keys())
        used_files = set()
        debug_obsolete = {}
        
        # Mark entry points as used
        for file_path in self.files_info.keys():
            if self.files_info[file_path]['is_entry_point']:
                used_files.add(self.normalize_path(file_path))
        
        # Mark files that are imported or referenced
        for file_path, imports in self.imports_map.items():
            norm_file_path = self.normalize_path(file_path)
            for imp in imports:
                # Try both relative and absolute resolution
                resolved_path = self.normalize_path(self.resolve_import_to_path(file_path, imp))
                if resolved_path in all_files:
                    used_files.add(resolved_path)
                # Also try the old logic for safety
                potential_files = [
                    f"{imp.replace('.', '/')}.py",
                    f"{imp.replace('.', '/')}" + "/__init__.py",
                    f"n8n_builder/{imp.replace('.', '/')}.py"
                ]
                for pot_file in potential_files:
                    norm_pot_file = self.normalize_path(pot_file)
                    if norm_pot_file in all_files:
                        used_files.add(norm_pot_file)
        
        # Mark files referenced by usage_map
        for file_path, references in self.usage_map.items():
            for ref in references:
                used_files.add(self.normalize_path(ref))
            if references:  # If file references others, it's probably used
                used_files.add(self.normalize_path(file_path))
        
        # Special cases - files that are used but might not show up in imports
        special_cases = {
            'static/index.html',  # Served by web server
            'setup.py',  # Installation script
            'requirements.txt',  # Dependencies
            'README.md',  # Documentation
            'Documentation/',  # Documentation files
        }
        for file_path in self.files_info.keys():
            norm_file_path = self.normalize_path(file_path)
            for special in special_cases:
                if special.lower() in norm_file_path:
                    used_files.add(norm_file_path)
                    break
        
        # --- DYNAMIC IMPORTS ---
        dynamic_imports = self.find_dynamic_imports()
        dynamic_used_files = set()
        for dyn in dynamic_imports:
            py_path = self.normalize_path(dyn.replace('.', '/') + '.py')
            if py_path in all_files:
                dynamic_used_files.add(py_path)
            else:
                norm_dyn = self.normalize_path(dyn)
                if norm_dyn in all_files:
                    dynamic_used_files.add(norm_dyn)
        if dynamic_used_files:
            print(f"🔎 Detected dynamic imports: {dynamic_used_files}")
        used_files.update(dynamic_used_files)
        self.dynamic_imports = list(dynamic_used_files)
        # --- END DYNAMIC IMPORTS ---
        
        # --- CRITICAL FILES WHITELIST ---
        critical_files = {
            'n8n_builder/config.py',
            'n8n_builder/settings.py',
            'n8n_builder/__init__.py',
            'config.py',
            'settings.py',
        }
        norm_critical_files = set(self.normalize_path(f) for f in critical_files)
        for crit in norm_critical_files:
            if crit in all_files:
                used_files.add(crit)
        # --- END CRITICAL FILES WHITELIST ---
        
        # Files that might be obsolete
        potentially_obsolete = all_files - used_files
        
        # Additional analysis for Python files
        for file_path in potentially_obsolete:
            orig_file_path = None
            for k in self.files_info.keys():
                if self.normalize_path(k) == file_path:
                    orig_file_path = k
                    break
            if orig_file_path and self.files_info[orig_file_path]['extension'] == '.py':
                try:
                    with open(self.files_info[orig_file_path]['path'], 'r', encoding='utf-8') as f:
                        content = f.read()
                    if 'if __name__ == "__main__"' in content:
                        used_files.add(file_path)  # Standalone script
                    elif 'def main(' in content:
                        used_files.add(file_path)  # Has main function
                except Exception:
                    pass
        self.obsolete_files = all_files - used_files
        # Debug output for why files are marked obsolete
        for file_path in self.obsolete_files:
            reasons = []
            if file_path in norm_critical_files:
                reasons.append('Critical file (whitelisted)')
            orig_file_path = None
            for k in self.files_info.keys():
                if self.normalize_path(k) == file_path:
                    orig_file_path = k
                    break
            if orig_file_path and self.files_info[orig_file_path]['is_entry_point']:
                reasons.append('Entry point')
            if file_path in dynamic_used_files:
                reasons.append('Dynamically imported')
            if not reasons:
                reasons.append('Not imported, referenced, or whitelisted')
            debug_obsolete[file_path] = reasons
        self.debug_obsolete = debug_obsolete

    def find_duplicates(self):
        """Find duplicate files by content."""
        print("🔍 Finding duplicate files...")
        
        # Remove entries with only one file
        self.duplicates = {k: v for k, v in self.duplicates.items() if len(v) > 1}

    def generate_report(self):
        """Generate comprehensive analysis report."""
        print("\n" + "="*80)
        print("📊 N8N BUILDER PROJECT FILE ANALYSIS REPORT")
        print("="*80)
        
        # Summary statistics
        total_files = len(self.files_info)
        total_size = sum(info['size'] for info in self.files_info.values())
        python_files = sum(1 for info in self.files_info.values() if info['extension'] == '.py')
        
        print(f"\n📈 SUMMARY STATISTICS:")
        print(f"   Total Files: {total_files}")
        print(f"   Total Size: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
        print(f"   Python Files: {python_files}")
        print(f"   Duplicate Groups: {len(self.duplicates)}")
        print(f"   Potentially Obsolete: {len(self.obsolete_files)}")
        
        # File type breakdown
        extensions = defaultdict(int)
        for info in self.files_info.values():
            extensions[info['extension'] or 'no extension'] += 1
        
        print(f"\n📁 FILE TYPES:")
        for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
            print(f"   {ext}: {count} files")
        
        # Duplicate files
        if self.duplicates:
            print(f"\n🔄 DUPLICATE FILES:")
            for file_hash, files in self.duplicates.items():
                print(f"\n   Hash: {file_hash[:8]}...")
                for file_path in files:
                    orig_path = self.normalized_to_original.get(self.normalize_path(file_path), file_path)
                    info = self.files_info[orig_path]
                    size = info['size']
                    modified = info['modified']
                    print(f"     📄 {file_path} ({size:,} bytes, modified: {modified.strftime('%Y-%m-%d %H:%M')})")
                
                # Recommend which to keep
                files_with_info = [(f, self.files_info[f]) for f in files]
                # Prefer entry points, then most recently modified
                recommended = max(files_with_info, 
                                key=lambda x: (x[1]['is_entry_point'], x[1]['modified']))
                print(f"     ✅ RECOMMEND KEEPING: {recommended[0]}")
                
                for file_path in files:
                    if file_path != recommended[0]:
                        orig_path = self.normalized_to_original.get(self.normalize_path(file_path), file_path)
                        size = self.files_info[orig_path]['size']
                        print(f"     ❌ CONSIDER REMOVING: {file_path}")
        else:
            print(f"\n🔄 DUPLICATE FILES: None found")
        
        # Obsolete files
        if self.obsolete_files:
            print(f"\n🗑️  POTENTIALLY OBSOLETE FILES:")
            
            # Group by directory for better organization
            obsolete_by_dir = defaultdict(list)
            for file_path in sorted(self.obsolete_files):
                dir_name = str(Path(file_path).parent)
                obsolete_by_dir[dir_name].append(file_path)
            
            for dir_name, files in sorted(obsolete_by_dir.items()):
                print(f"\n   📁 {dir_name}/")
                for file_path in files:
                    orig_path = self.normalized_to_original.get(self.normalize_path(file_path), file_path)
                    info = self.files_info[orig_path]
                    print(f"     ❓ {Path(file_path).name} ({info['size']:,} bytes, {info['extension']})")
                    
                    # Provide reasoning
                    if info['extension'] == '.py':
                        print(f"        Reason: No imports found, not an entry point")
                    else:
                        print(f"        Reason: No references found in code")
        else:
            print(f"\n🗑️  POTENTIALLY OBSOLETE FILES: None found")
        
        # Entry points analysis
        print(f"\n🚀 ENTRY POINTS:")
        for file_path, info in self.files_info.items():
            if info['is_entry_point']:
                print(f"   ✅ {file_path}")
        
        # Large files
        large_files = [(path, info) for path, info in self.files_info.items() 
                      if info['size'] > 100000]  # > 100KB
        if large_files:
            print(f"\n📦 LARGE FILES (>100KB):")
            for file_path, info in sorted(large_files, key=lambda x: x[1]['size'], reverse=True):
                print(f"   📄 {file_path}: {info['size']:,} bytes ({info['size']/1024/1024:.2f} MB)")
        
        # Add dynamic imports to the report
        if hasattr(self, 'dynamic_imports') and self.dynamic_imports:
            print(f"\n🔎 DYNAMIC IMPORTS DETECTED (not marked obsolete):")
            for dyn in self.dynamic_imports:
                print(f"   - {dyn}")
        # Add debug output for obsolete files
        if hasattr(self, 'debug_obsolete'):
            print(f"\n🛑 DEBUG: Why files are marked obsolete:")
            for file_path, reasons in self.debug_obsolete.items():
                print(f"   {file_path}: {', '.join(reasons)}")
        
        # Cleanup recommendations
        print(f"\n🧹 CLEANUP RECOMMENDATIONS:")
        
        total_duplicate_waste = 0
        if self.duplicates:
            print(f"\n   1. REMOVE DUPLICATE FILES:")
            for file_hash, files in self.duplicates.items():
                files_with_info = [(f, self.files_info[f]) for f in files]
                recommended = max(files_with_info, 
                                key=lambda x: (x[1]['is_entry_point'], x[1]['modified']))
                for file_path in files:
                    if file_path != recommended[0]:
                        orig_path = self.normalized_to_original.get(self.normalize_path(file_path), file_path)
                        size = self.files_info[orig_path]['size']
                        total_duplicate_waste += size
                        print(f"      rm \"{file_path}\"  # Saves {size:,} bytes")
        
        total_obsolete_waste = 0
        if self.obsolete_files:
            print(f"\n   2. REMOVE OBSOLETE FILES:")
            for file_path in sorted(self.obsolete_files):
                orig_path = self.normalized_to_original.get(self.normalize_path(file_path), file_path)
                size = self.files_info[orig_path]['size']
                total_obsolete_waste += size
                print(f"      rm \"{file_path}\"  # Saves {size:,} bytes")
        
        total_savings = total_duplicate_waste + total_obsolete_waste
        if total_savings > 0:
            print(f"\n   💾 TOTAL POTENTIAL SAVINGS: {total_savings:,} bytes ({total_savings/1024/1024:.2f} MB)")
        
        print(f"\n   3. GENERAL RECOMMENDATIONS:")
        if any('.egg-info' in path for path in self.files_info.keys()):
            print(f"      - Remove .egg-info directories (development artifacts)")
        if any('__pycache__' in str(info['path']) for info in self.files_info.values()):
            print(f"      - Remove __pycache__ directories (compiled Python)")
        
        print(f"\n⚠️  IMPORTANT NOTES:")
        print(f"   - Review obsolete files manually before deletion")
        print(f"   - Some files may be used by external tools or scripts")
        print(f"   - Test thoroughly after any cleanup")
        print(f"   - Consider version control before making changes")

    def save_detailed_report(self, filename: str = "project_analysis_report.json"):
        """Save detailed analysis to JSON file."""
        report_data = {
            'analysis_date': datetime.datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'summary': {
                'total_files': len(self.files_info),
                'total_size': sum(info['size'] for info in self.files_info.values()),
                'duplicate_groups': len(self.duplicates),
                'obsolete_files': len(self.obsolete_files)
            },
            'files': {
                path: {
                    'size': info['size'],
                    'modified': info['modified'].isoformat(),
                    'hash': info['hash'],
                    'extension': info['extension'],
                    'is_entry_point': info['is_entry_point']
                }
                for path, info in self.files_info.items()
            },
            'duplicates': dict(self.duplicates),
            'obsolete_files': list(self.obsolete_files),
            'imports_map': {k: list(v) for k, v in self.imports_map.items()},
            'usage_map': {k: list(v) for k, v in self.usage_map.items()}
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"\n💾 Detailed report saved to: {filename}")

    def save_markdown_report(self, filename: str = "project_analysis_report.md"):
        """Save detailed analysis to Markdown file with DOS commands."""
        md_content = []
        
        # Header
        md_content.append("# N8N Builder Project File Analysis Report")
        md_content.append(f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_content.append(f"**Project Root:** `{self.project_root}`")
        md_content.append("")
        
        # Summary statistics
        total_files = len(self.files_info)
        total_size = sum(info['size'] for info in self.files_info.values())
        python_files = sum(1 for info in self.files_info.values() if info['extension'] == '.py')
        
        md_content.append("## 📈 Summary Statistics")
        md_content.append("")
        md_content.append(f"- **Total Files:** {total_files:,}")
        md_content.append(f"- **Total Size:** {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
        md_content.append(f"- **Python Files:** {python_files:,}")
        md_content.append(f"- **Duplicate Groups:** {len(self.duplicates):,}")
        md_content.append(f"- **Potentially Obsolete:** {len(self.obsolete_files):,}")
        md_content.append("")
        
        # File type breakdown
        extensions = defaultdict(int)
        for info in self.files_info.values():
            extensions[info['extension'] or 'no extension'] += 1
        
        md_content.append("## 📁 File Types")
        md_content.append("")
        md_content.append("| Extension | Count |")
        md_content.append("|-----------|-------|")
        for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
            md_content.append(f"| `{ext}` | {count:,} |")
        md_content.append("")
        
        # Entry points
        md_content.append("## 🚀 Entry Points")
        md_content.append("")
        entry_points_found = [path for path, info in self.files_info.items() if info['is_entry_point']]
        if entry_points_found:
            for file_path in entry_points_found:
                md_content.append(f"- ✅ `{file_path}`")
        else:
            md_content.append("- No entry points found")
        md_content.append("")
        
        # Large files
        large_files = [(path, info) for path, info in self.files_info.items() 
                      if info['size'] > 100000]  # > 100KB
        if large_files:
            md_content.append("## 📦 Large Files (>100KB)")
            md_content.append("")
            md_content.append("| File | Size (bytes) | Size (MB) |")
            md_content.append("|------|--------------|-----------|")
            for file_path, info in sorted(large_files, key=lambda x: x[1]['size'], reverse=True):
                size_mb = info['size']/1024/1024
                md_content.append(f"| `{file_path}` | {info['size']:,} | {size_mb:.2f} |")
            md_content.append("")
        
        # Duplicate files
        if self.duplicates:
            md_content.append("## 🔄 Duplicate Files")
            md_content.append("")
            
            for i, (file_hash, files) in enumerate(self.duplicates.items(), 1):
                md_content.append(f"### Duplicate Group {i}")
                md_content.append(f"**Hash:** `{file_hash[:16]}...`")
                md_content.append("")
                
                # Show all files in group
                md_content.append("| File | Size | Modified | Recommendation |")
                md_content.append("|------|------|----------|----------------|")
                
                files_with_info = [(f, self.files_info[f]) for f in files]
                recommended = max(files_with_info, 
                                key=lambda x: (x[1]['is_entry_point'], x[1]['modified']))
                
                for file_path in files:
                    orig_path = self.normalized_to_original.get(self.normalize_path(file_path), file_path)
                    info = self.files_info[orig_path]
                    size = info['size']
                    modified = info['modified'].strftime('%Y-%m-%d %H:%M')
                    
                    if file_path == recommended[0]:
                        recommendation = "✅ **KEEP**"
                    else:
                        recommendation = "❌ Remove"
                    
                    md_content.append(f"| `{file_path}` | {size:,} | {modified} | {recommendation} |")
                
                md_content.append("")
        else:
            md_content.append("## 🔄 Duplicate Files")
            md_content.append("")
            md_content.append("✅ No duplicate files found.")
            md_content.append("")
        
        # Obsolete files
        if self.obsolete_files:
            md_content.append("## 🗑️ Potentially Obsolete Files")
            md_content.append("")
            
            # Group by directory
            obsolete_by_dir = defaultdict(list)
            for file_path in sorted(self.obsolete_files):
                dir_name = str(Path(file_path).parent)
                obsolete_by_dir[dir_name].append(file_path)
            
            for dir_name, files in sorted(obsolete_by_dir.items()):
                md_content.append(f"### Directory: `{dir_name}/`")
                md_content.append("")
                md_content.append("| File | Size | Extension | Reason |")
                md_content.append("|------|------|-----------|--------|")
                
                for file_path in files:
                    orig_path = self.normalized_to_original.get(self.normalize_path(file_path), file_path)
                    info = self.files_info[orig_path]
                    filename = Path(file_path).name
                    
                    if info['extension'] == '.py':
                        reason = "No imports found, not an entry point"
                    else:
                        reason = "No references found in code"
                    
                    md_content.append(f"| `{filename}` | {info['size']:,} | `{info['extension']}` | {reason} |")
                
                md_content.append("")
        else:
            md_content.append("## 🗑️ Potentially Obsolete Files")
            md_content.append("")
            md_content.append("✅ No potentially obsolete files found.")
            md_content.append("")
        
        # DOS Commands for cleanup
        md_content.append("## 🧹 Cleanup Commands")
        md_content.append("")
        md_content.append("### Setup Archive Directory")
        md_content.append("```batch")
        md_content.append("REM Create archive directory if it doesn't exist")
        md_content.append("if not exist \"Archive\" mkdir Archive")
        md_content.append("if not exist \"Archive\\Duplicates\" mkdir Archive\\Duplicates")
        md_content.append("if not exist \"Archive\\Obsolete\" mkdir Archive\\Obsolete")
        md_content.append("```")
        md_content.append("")
        
        # Calculate potential savings
        total_duplicate_waste = 0
        total_obsolete_waste = 0
        
        if self.duplicates:
            md_content.append("### Move Duplicate Files to Archive")
            md_content.append("```batch")
            md_content.append("REM Move duplicate files to archive (keeping the recommended version)")
            
            for file_hash, files in self.duplicates.items():
                files_with_info = [(f, self.files_info[f]) for f in files]
                recommended = max(files_with_info, 
                                key=lambda x: (x[1]['is_entry_point'], x[1]['modified']))
                
                md_content.append(f"")
                md_content.append(f"REM Duplicate group: {file_hash[:8]}...")
                md_content.append(f"REM Keeping: {recommended[0]}")
                
                for file_path in files:
                    if file_path != recommended[0]:
                        orig_path = self.normalized_to_original.get(self.normalize_path(file_path), file_path)
                        size = self.files_info[orig_path]['size']
                        total_duplicate_waste += size
                        
                        # Convert forward slashes to backslashes for Windows
                        win_path = file_path.replace('/', '\\')
                        archive_path = f"Archive\\Duplicates\\{Path(file_path).name}"
                        
                        md_content.append(f"move \"{win_path}\" \"{archive_path}\"")
            
            md_content.append("```")
            md_content.append("")
        
        if self.obsolete_files:
            md_content.append("### Move Obsolete Files to Archive")
            md_content.append("```batch")
            md_content.append("REM Move potentially obsolete files to archive")
            
            for file_path in sorted(self.obsolete_files):
                orig_path = self.normalized_to_original.get(self.normalize_path(file_path), file_path)
                size = self.files_info[orig_path]['size']
                total_obsolete_waste += size
                
                # Convert forward slashes to backslashes for Windows
                win_path = file_path.replace('/', '\\')
                archive_path = f"Archive\\Obsolete\\{Path(file_path).name}"
                
                md_content.append(f"move \"{win_path}\" \"{archive_path}\"")
            
            md_content.append("```")
            md_content.append("")
        
        # Summary of potential savings
        total_savings = total_duplicate_waste + total_obsolete_waste
        if total_savings > 0:
            md_content.append("### Potential Space Savings")
            md_content.append("")
            md_content.append(f"- **Duplicate files:** {total_duplicate_waste:,} bytes ({total_duplicate_waste/1024/1024:.2f} MB)")
            md_content.append(f"- **Obsolete files:** {total_obsolete_waste:,} bytes ({total_obsolete_waste/1024/1024:.2f} MB)")
            md_content.append(f"- **Total potential savings:** {total_savings:,} bytes ({total_savings/1024/1024:.2f} MB)")
            md_content.append("")
        
        # General recommendations
        md_content.append("### General Cleanup Recommendations")
        md_content.append("")
        md_content.append("```batch")
        md_content.append("REM Remove development artifacts")
        
        if any('.egg-info' in path for path in self.files_info.keys()):
            md_content.append("rmdir /s /q n8n_builder.egg-info")
        
        if any('__pycache__' in str(info['path']) for info in self.files_info.values()):
            md_content.append("for /d /r . %%d in (__pycache__) do @if exist \"%%d\" rmdir /s /q \"%%d\"")
        
        md_content.append("```")
        md_content.append("")
        
        # Important notes
        md_content.append("## ⚠️ Important Notes")
        md_content.append("")
        md_content.append("- **Review before execution:** Manually review all obsolete files before moving them")
        md_content.append("- **External dependencies:** Some files may be used by external tools or scripts")
        md_content.append("- **Test thoroughly:** Test the application after any cleanup")
        md_content.append("- **Version control:** Consider committing current state before making changes")
        md_content.append("- **Archive first:** Files are moved to Archive folder, not deleted permanently")
        md_content.append("- **Recovery:** You can restore files from Archive if needed")
        md_content.append("")
        
        # Restore commands
        md_content.append("## 🔄 Recovery Commands")
        md_content.append("")
        md_content.append("If you need to restore files from the archive:")
        md_content.append("")
        md_content.append("```batch")
        md_content.append("REM Restore all duplicates")
        md_content.append("move Archive\\Duplicates\\* .")
        md_content.append("")
        md_content.append("REM Restore all obsolete files")
        md_content.append("move Archive\\Obsolete\\* .")
        md_content.append("")
        md_content.append("REM Remove empty archive directories")
        md_content.append("rmdir Archive\\Duplicates")
        md_content.append("rmdir Archive\\Obsolete")
        md_content.append("rmdir Archive")
        md_content.append("```")
        md_content.append("")
        
        # Write markdown file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))
        
        print(f"📝 Markdown report saved to: {filename}")

    def run_analysis(self):
        """Run complete project analysis."""
        print("🚀 Starting N8N Builder Project Analysis...")
        
        self.scan_all_files()
        self.analyze_dependencies()
        self.find_duplicates()
        self.identify_obsolete_files()
        self.generate_report()
        self.save_detailed_report()
        self.save_markdown_report()
        
        print(f"\n✅ Analysis complete!")

def main():
    """Main function."""
    analyzer = ProjectAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main() 