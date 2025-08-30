# Table Name Fixer Guide

## Overview

The Table Name Fixer scripts provide automated solutions for fixing table name references across your codebase using the database repair summary CSV files. This is particularly useful when you need to rename tables to follow naming conventions and propagate those changes throughout your code.

## Scripts Available

### 1. `fix_table_names.py` - Single Table Name Fixer

Fixes a single table name mapping across the codebase.

**Usage:**
```bash
python Scripts/fix_table_names.py <csv_file> <old_table_name> <new_table_name>
```

**Example:**
```bash
python Scripts/fix_table_names.py data/database_repair_logs/repair_summary_20250823_110612.csv XRF_EntityAttributeValue XRF_Entity_AttributeValue
```

### 2. `batch_fix_table_names.py` - Batch Table Name Fixer

Processes multiple table name mappings from a JSON configuration file.

**Usage:**
```bash
python Scripts/batch_fix_table_names.py <csv_file> <mapping_file>
```

**Create Sample Mapping File:**
```bash
python Scripts/batch_fix_table_names.py --create-sample table_mappings.json
```

**Example:**
```bash
python Scripts/batch_fix_table_names.py repair_summary.csv table_mappings.json
```

## How It Works

### Process Flow

1. **CSV Analysis**: The script reads the database repair summary CSV file
2. **Entry Filtering**: Finds entries that contain references to the old table name
3. **Smart Search**: Searches around the reported line numbers (±5 lines) to catch nearby references
4. **Pattern Matching**: Uses word boundary regex to ensure accurate replacements
5. **File Updates**: Updates the source files with the new table names
6. **Reporting**: Generates detailed reports of all changes made

### Key Features

- **Smart Line Detection**: Searches around reported line numbers to catch references that might be on adjacent lines
- **Duplicate Prevention**: Avoids processing the same file/line combination multiple times
- **Word Boundary Matching**: Uses regex word boundaries to prevent partial matches
- **Comprehensive Reporting**: Generates detailed logs of all changes made
- **Error Handling**: Provides clear error messages for missing files or invalid data

## Configuration Files

### Mapping File Format (JSON)

```json
{
  "XRF_EntityAttributeValue": "XRF_Entity_AttributeValue",
  "REF_OldTable": "REF_New_Table",
  "XRF_AnotherTable": "XRF_Another_Table"
}
```

## Workflow Integration

### Typical Usage Pattern

1. **Run Database Validation**: Execute your database repair process to generate a CSV summary
2. **Identify Issues**: Review the CSV for table name errors
3. **Create Mappings**: Either use single fixes or create a batch mapping file
4. **Apply Fixes**: Run the appropriate fixer script
5. **Verify Results**: Review the generated reports
6. **Re-run Validation**: Execute the database repair process again to confirm fixes

### Example Workflow

```bash
# Step 1: Run database validation (generates CSV)
python Scripts/enhanced_database_fixer.py

# Step 2: Fix table names using the generated CSV
python Scripts/fix_table_names.py data/database_repair_logs/repair_summary_latest.csv XRF_EntityAttributeValue XRF_Entity_AttributeValue

# Step 3: Re-run validation to confirm fixes
python Scripts/enhanced_database_fixer.py
```

## Output and Reporting

### Report Files

The scripts generate detailed reports in `data/database_repair_logs/`:

- **Single Fix**: `table_name_fixes_YYYYMMDD_HHMMSS.txt`
- **Batch Fix**: `batch_table_fixes_YYYYMMDD_HHMMSS.txt`

### Report Contents

- **Summary Statistics**: Number of fixes applied and errors encountered
- **Detailed Changes**: Line-by-line breakdown of all modifications
- **Error Log**: Any issues encountered during processing
- **File Locations**: Complete paths to all modified files

## Best Practices

### Before Running

1. **Backup Your Code**: Ensure you have version control or backups
2. **Review CSV Data**: Understand what table name issues exist
3. **Test on Small Set**: Try with a single table name first
4. **Verify Mappings**: Double-check your old/new table name mappings

### After Running

1. **Review Reports**: Check the generated reports for accuracy
2. **Test Your Code**: Run your application to ensure changes work correctly
3. **Re-run Validation**: Confirm that the database validation now passes
4. **Commit Changes**: Save your fixes to version control

## Troubleshooting

### Common Issues

**No Changes Applied**
- Check if the table name already exists in the correct form
- Verify the CSV file contains entries for the specified table
- Ensure file paths in the CSV are correct and accessible

**Partial Fixes**
- The script searches ±5 lines around reported line numbers
- Some references might be further away and require manual fixing
- Check the report for which files were processed

**File Not Found Errors**
- Verify all file paths in the CSV are correct
- Ensure you're running from the correct working directory
- Check file permissions

### Advanced Usage

**Custom Search Range**
The script searches ±5 lines around reported line numbers. This can be adjusted in the code if needed.

**Regex Patterns**
The script uses word boundary matching (`\b`) to ensure accurate replacements. This prevents partial matches but requires exact word matches.

## Integration with Database Validation

These scripts are designed to work seamlessly with the database validation system:

1. **Database Validator** identifies table name issues and logs them to CSV
2. **Table Name Fixer** uses the CSV to systematically fix the issues
3. **Re-validation** confirms that the fixes resolved the problems

This creates a complete maintenance workflow for keeping your database schema and code in sync.
