import os
import shutil
import json
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.resolve()
ARCHIVE_OBSOLETE = PROJECT_ROOT / 'Archive' / 'Obsolete'
ARCHIVE_DUPLICATES = PROJECT_ROOT / 'Archive' / 'Duplicates'
ANALYSIS_REPORT = PROJECT_ROOT / 'project_analysis_report.json'
LOG_FILE = PROJECT_ROOT / 'safe_cleanup_moves.log'
RESTORE_SCRIPT = PROJECT_ROOT / 'RestoreMoves.bat'

# Ensure archive directories exist
def ensure_dir(path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

ensure_dir(ARCHIVE_OBSOLETE)
ensure_dir(ARCHIVE_DUPLICATES)

# Load analysis report
with open(ANALYSIS_REPORT, 'r', encoding='utf-8') as f:
    report = json.load(f)

obsolete_files = set(report.get('obsolete_files', []))
duplicates = report.get('duplicates', {})
files_info = report.get('files', {})

# Find duplicate files to move (excluding the recommended 'keep' version)
duplicate_files_to_move = set()
for file_hash, files in duplicates.items():
    # Find the recommended file to keep (entry point or most recently modified)
    files_with_info = [(f, files_info.get(f, {})) for f in files]
    recommended = max(files_with_info, key=lambda x: (x[1].get('is_entry_point', False), x[1].get('modified', '')))[0]
    for file_path in files:
        if file_path != recommended:
            duplicate_files_to_move.add(file_path)

# Prepare log and restore script
move_log = []
restore_cmds = []

# Move obsolete files
for rel_path in obsolete_files:
    src = PROJECT_ROOT / rel_path
    dst = ARCHIVE_OBSOLETE / rel_path
    if src.exists():
        ensure_dir(dst.parent)
        shutil.move(str(src), str(dst))
        move_log.append(f"OBSOLETE: {src} -> {dst}")
        restore_cmds.append(f'move "{dst}" "{src}"')

# Move duplicate files
for rel_path in duplicate_files_to_move:
    src = PROJECT_ROOT / rel_path
    dst = ARCHIVE_DUPLICATES / rel_path
    if src.exists():
        ensure_dir(dst.parent)
        shutil.move(str(src), str(dst))
        move_log.append(f"DUPLICATE: {src} -> {dst}")
        restore_cmds.append(f'move "{dst}" "{src}"')

# Write log
with open(LOG_FILE, 'w', encoding='utf-8') as f:
    for line in move_log:
        f.write(line + '\n')

# Write restore script
with open(RESTORE_SCRIPT, 'w', encoding='utf-8') as f:
    f.write("@echo off\n")
    f.write("REM Restore all moved files to their original locations\n")
    for cmd in restore_cmds:
        f.write(cmd + '\n')
    f.write("echo Restore complete.\n")

print(f"Moved {len(obsolete_files)} obsolete files and {len(duplicate_files_to_move)} duplicate files.")
print(f"Log written to {LOG_FILE}")
print(f"Restore script written to {RESTORE_SCRIPT}") 