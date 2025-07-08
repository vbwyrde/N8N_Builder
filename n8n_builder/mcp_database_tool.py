"""
MCP Database Tool for SQL Server Integration
Provides Model Context Protocol interface for database operations.
"""

import asyncio
import logging
import pyodbc
import decimal
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json

from .config import config

logger = logging.getLogger(__name__)


@dataclass
class DatabaseSchema:
    """Represents database schema information."""
    database_name: str
    tables: List[Dict[str, Any]]
    views: List[Dict[str, Any]]
    procedures: List[Dict[str, Any]]
    functions: List[Dict[str, Any]]


@dataclass
class TableInfo:
    """Represents table structure information."""
    table_name: str
    schema_name: str
    columns: List[Dict[str, Any]]
    indexes: List[Dict[str, Any]]
    foreign_keys: List[Dict[str, Any]]
    row_count: Optional[int] = None


class MCPDatabaseTool:
    """MCP Database Tool for SQL Server operations."""
    
    def __init__(self, connection_name: str = 'Enterprise_Database'):
        """Initialize the database tool with connection configuration."""
        self.connection_name = connection_name
        self.connection_config = config.mcp_database.connections.get(connection_name)
        
        if not self.connection_config:
            raise ValueError(f"Database connection '{connection_name}' not found in configuration")
        
        self.connection_string = self._build_connection_string()
        self.logger = logger
        
        self.logger.debug(f"MCP Database Tool initialized for connection: {connection_name}")
    
    def _build_connection_string(self) -> str:
        """Build SQL Server connection string from configuration."""
        config_dict = self.connection_config

        # Build connection string for SQL Server with trusted connection
        conn_parts = [
            f"DRIVER={{{config_dict['driver']}}}",
            f"SERVER={config_dict['server']}",
            f"DATABASE={config_dict['database']}",
            f"Trusted_Connection={config_dict['trusted_connection']}",
            f"Connection Timeout={config_dict['connection_timeout']}",
            f"Command Timeout={config_dict['command_timeout']}"
        ]

        # Add SSL/encryption settings if present
        if 'encrypt' in config_dict:
            conn_parts.append(f"Encrypt={config_dict['encrypt']}")
        if 'trust_server_certificate' in config_dict:
            conn_parts.append(f"TrustServerCertificate={config_dict['trust_server_certificate']}")

        return ";".join(conn_parts)
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test database connection and return status."""
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT @@VERSION as version, DB_NAME() as database_name, GETDATE() as connection_time")
                result = cursor.fetchone()

                return {
                    'status': 'success',
                    'connected': True,
                    'server_version': result.version,
                    'database_name': result.database_name,
                    'connection_time': result.connection_time.isoformat(),
                    'connection_string_used': self.connection_string.replace('Trusted_Connection=yes', 'Trusted_Connection=***')
                }
        except Exception as e:
            self.logger.error(f"Database connection test failed: {e}")
            return {
                'status': 'error',
                'connected': False,
                'error': str(e),
                'connection_string_used': self.connection_string.replace('Trusted_Connection=yes', 'Trusted_Connection=***')
            }
    
    async def get_database_schema(self) -> DatabaseSchema:
        """Get comprehensive database schema information."""
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                
                # Get database name
                cursor.execute("SELECT DB_NAME() as database_name")
                db_name = cursor.fetchone().database_name
                
                # Get tables
                tables = await self._get_tables(cursor)
                
                # Get views
                views = await self._get_views(cursor)
                
                # Get stored procedures
                procedures = await self._get_procedures(cursor)
                
                # Get functions
                functions = await self._get_functions(cursor)
                
                return DatabaseSchema(
                    database_name=db_name,
                    tables=tables,
                    views=views,
                    procedures=procedures,
                    functions=functions
                )
        except Exception as e:
            self.logger.error(f"Failed to get database schema: {e}")
            raise
    
    async def _get_tables(self, cursor) -> List[Dict[str, Any]]:
        """Get all tables in the database."""
        cursor.execute("""
            SELECT 
                TABLE_SCHEMA,
                TABLE_NAME,
                TABLE_TYPE
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """)
        
        tables = []
        for row in cursor.fetchall():
            tables.append({
                'schema': row.TABLE_SCHEMA,
                'name': row.TABLE_NAME,
                'type': row.TABLE_TYPE
            })
        
        return tables
    
    async def _get_views(self, cursor) -> List[Dict[str, Any]]:
        """Get all views in the database."""
        cursor.execute("""
            SELECT 
                TABLE_SCHEMA,
                TABLE_NAME
            FROM INFORMATION_SCHEMA.VIEWS
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """)
        
        views = []
        for row in cursor.fetchall():
            views.append({
                'schema': row.TABLE_SCHEMA,
                'name': row.TABLE_NAME,
                'type': 'VIEW'
            })
        
        return views
    
    async def _get_procedures(self, cursor) -> List[Dict[str, Any]]:
        """Get all stored procedures in the database."""
        cursor.execute("""
            SELECT 
                ROUTINE_SCHEMA,
                ROUTINE_NAME,
                ROUTINE_TYPE
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_TYPE = 'PROCEDURE'
            ORDER BY ROUTINE_SCHEMA, ROUTINE_NAME
        """)
        
        procedures = []
        for row in cursor.fetchall():
            procedures.append({
                'schema': row.ROUTINE_SCHEMA,
                'name': row.ROUTINE_NAME,
                'type': row.ROUTINE_TYPE
            })
        
        return procedures
    
    async def _get_functions(self, cursor) -> List[Dict[str, Any]]:
        """Get all functions in the database."""
        cursor.execute("""
            SELECT 
                ROUTINE_SCHEMA,
                ROUTINE_NAME,
                ROUTINE_TYPE
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_TYPE = 'FUNCTION'
            ORDER BY ROUTINE_SCHEMA, ROUTINE_NAME
        """)
        
        functions = []
        for row in cursor.fetchall():
            functions.append({
                'schema': row.ROUTINE_SCHEMA,
                'name': row.ROUTINE_NAME,
                'type': row.ROUTINE_TYPE
            })
        
        return functions
    
    async def get_table_info(self, table_name: str, schema_name: str = 'dbo') -> TableInfo:
        """Get detailed information about a specific table."""
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                
                # Get columns
                columns = await self._get_table_columns(cursor, table_name, schema_name)
                
                # Get indexes
                indexes = await self._get_table_indexes(cursor, table_name, schema_name)
                
                # Get foreign keys
                foreign_keys = await self._get_table_foreign_keys(cursor, table_name, schema_name)
                
                # Get row count
                row_count = await self._get_table_row_count(cursor, table_name, schema_name)
                
                return TableInfo(
                    table_name=table_name,
                    schema_name=schema_name,
                    columns=columns,
                    indexes=indexes,
                    foreign_keys=foreign_keys,
                    row_count=row_count
                )
        except Exception as e:
            self.logger.error(f"Failed to get table info for {schema_name}.{table_name}: {e}")
            raise
    
    async def _get_table_columns(self, cursor, table_name: str, schema_name: str) -> List[Dict[str, Any]]:
        """Get column information for a table."""
        cursor.execute("""
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                COLUMN_DEFAULT,
                CHARACTER_MAXIMUM_LENGTH,
                NUMERIC_PRECISION,
                NUMERIC_SCALE,
                ORDINAL_POSITION
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = ? AND TABLE_SCHEMA = ?
            ORDER BY ORDINAL_POSITION
        """, table_name, schema_name)
        
        columns = []
        for row in cursor.fetchall():
            columns.append({
                'name': row.COLUMN_NAME,
                'data_type': row.DATA_TYPE,
                'is_nullable': row.IS_NULLABLE == 'YES',
                'default_value': row.COLUMN_DEFAULT,
                'max_length': row.CHARACTER_MAXIMUM_LENGTH,
                'precision': row.NUMERIC_PRECISION,
                'scale': row.NUMERIC_SCALE,
                'position': row.ORDINAL_POSITION
            })
        
        return columns

    async def _get_table_indexes(self, cursor, table_name: str, schema_name: str) -> List[Dict[str, Any]]:
        """Get index information for a table."""
        cursor.execute("""
            SELECT
                i.name as index_name,
                i.type_desc as index_type,
                i.is_unique,
                i.is_primary_key,
                STRING_AGG(c.name, ', ') WITHIN GROUP (ORDER BY ic.key_ordinal) as columns
            FROM sys.indexes i
            INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
            INNER JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
            INNER JOIN sys.tables t ON i.object_id = t.object_id
            INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
            WHERE t.name = ? AND s.name = ?
            GROUP BY i.name, i.type_desc, i.is_unique, i.is_primary_key
            ORDER BY i.name
        """, table_name, schema_name)

        indexes = []
        for row in cursor.fetchall():
            indexes.append({
                'name': row.index_name,
                'type': row.index_type,
                'is_unique': row.is_unique,
                'is_primary_key': row.is_primary_key,
                'columns': row.columns
            })

        return indexes

    async def _get_table_foreign_keys(self, cursor, table_name: str, schema_name: str) -> List[Dict[str, Any]]:
        """Get foreign key information for a table."""
        cursor.execute("""
            SELECT
                fk.name as foreign_key_name,
                OBJECT_SCHEMA_NAME(fk.parent_object_id) as schema_name,
                OBJECT_NAME(fk.parent_object_id) as table_name,
                COL_NAME(fkc.parent_object_id, fkc.parent_column_id) as column_name,
                OBJECT_SCHEMA_NAME(fk.referenced_object_id) as referenced_schema,
                OBJECT_NAME(fk.referenced_object_id) as referenced_table,
                COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) as referenced_column
            FROM sys.foreign_keys fk
            INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
            WHERE OBJECT_NAME(fk.parent_object_id) = ? AND OBJECT_SCHEMA_NAME(fk.parent_object_id) = ?
            ORDER BY fk.name
        """, table_name, schema_name)

        foreign_keys = []
        for row in cursor.fetchall():
            foreign_keys.append({
                'name': row.foreign_key_name,
                'column': row.column_name,
                'referenced_schema': row.referenced_schema,
                'referenced_table': row.referenced_table,
                'referenced_column': row.referenced_column
            })

        return foreign_keys

    async def _get_table_row_count(self, cursor, table_name: str, schema_name: str) -> Optional[int]:
        """Get approximate row count for a table."""
        try:
            cursor.execute(f"SELECT COUNT(*) as row_count FROM [{schema_name}].[{table_name}]")
            result = cursor.fetchone()
            return result.row_count if result else None
        except Exception as e:
            self.logger.warning(f"Could not get row count for {schema_name}.{table_name}: {e}")
            return None

    async def execute_query(self, query: str, parameters: Optional[List] = None) -> Dict[str, Any]:
        """Execute a SQL query and return results."""
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()

                if parameters:
                    cursor.execute(query, parameters)
                else:
                    cursor.execute(query)

                # Check if this is a query that returns results (SELECT, EXEC, or INSERT with OUTPUT)
                query_upper = query.strip().upper()
                returns_data = (query_upper.startswith('SELECT') or
                               query_upper.startswith('EXEC') or
                               ('INSERT' in query_upper and 'OUTPUT' in query_upper))

                if returns_data:
                    all_rows = []
                    result_set_count = 0

                    # Handle multiple result sets (especially for stored procedures)
                    while True:
                        if cursor.description:  # Check if current result set has columns
                            columns = [desc[0] for desc in cursor.description]
                            result_set_count += 1

                            # Fetch all rows from current result set
                            for row in cursor.fetchall():
                                row_dict = {}
                                for i, value in enumerate(row):
                                    # Handle datetime objects
                                    if isinstance(value, datetime):
                                        row_dict[columns[i]] = value.isoformat()
                                    else:
                                        row_dict[columns[i]] = value
                                all_rows.append(row_dict)

                        # Try to move to next result set
                        try:
                            if not cursor.nextset():
                                break
                        except Exception:
                            # No more result sets or nextset() not supported
                            break

                    # Determine query type
                    if query_upper.startswith('SELECT'):
                        query_type = 'SELECT'
                    elif query_upper.startswith('EXEC'):
                        query_type = 'EXEC'
                    elif 'INSERT' in query_upper and 'OUTPUT' in query_upper:
                        query_type = 'INSERT_OUTPUT'
                    else:
                        query_type = 'UNKNOWN'

                    return {
                        'status': 'success',
                        'query_type': query_type,
                        'rows': all_rows,
                        'row_count': len(all_rows),
                        'result_set_count': result_set_count
                    }
                else:
                    # For non-SELECT queries
                    rows_affected = cursor.rowcount
                    conn.commit()

                    return {
                        'status': 'success',
                        'query_type': 'MODIFY',
                        'rows_affected': rows_affected
                    }

        except Exception as e:
            self.logger.error(f"Query execution failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'query': query
            }

    async def get_sample_data(self, table_name: str, schema_name: str = 'dbo', limit: int = 10) -> Dict[str, Any]:
        """Get sample data from a table."""
        query = f"SELECT TOP {limit} * FROM [{schema_name}].[{table_name}]"
        return await self.execute_query(query)

    async def execute_stored_procedure(self, procedure_name: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a stored procedure with named parameters."""
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()

                # Build the EXEC statement with named parameters
                if parameters:
                    param_list = []
                    param_values = []

                    for param_name, param_value in parameters.items():
                        # Ensure parameter name starts with @
                        if not param_name.startswith('@'):
                            param_name = f"@{param_name}"
                        param_list.append(f"{param_name} = ?")
                        param_values.append(param_value)

                    exec_statement = f"EXEC {procedure_name} {', '.join(param_list)}"
                    cursor.execute(exec_statement, param_values)
                else:
                    exec_statement = f"EXEC {procedure_name}"
                    cursor.execute(exec_statement)

                # Handle multiple result sets
                all_result_sets = []
                result_set_count = 0

                while True:
                    try:
                        # Get column information
                        columns = [column[0] for column in cursor.description] if cursor.description else []

                        if columns:
                            # Fetch all rows for this result set
                            rows = []
                            while True:
                                row = cursor.fetchone()
                                if row is None:
                                    break

                                # Convert row to dictionary
                                row_dict = {}
                                for i, value in enumerate(row):
                                    if isinstance(value, datetime):
                                        row_dict[columns[i]] = value.isoformat()
                                    elif isinstance(value, decimal.Decimal):
                                        row_dict[columns[i]] = float(value)
                                    else:
                                        row_dict[columns[i]] = value
                                rows.append(row_dict)

                            all_result_sets.append({
                                'result_set_index': result_set_count,
                                'columns': columns,
                                'rows': rows,
                                'row_count': len(rows)
                            })
                            result_set_count += 1

                        # Try to move to next result set
                        if not cursor.nextset():
                            break

                    except Exception as e:
                        # No more result sets
                        break

                return {
                    'status': 'success',
                    'procedure_name': procedure_name,
                    'parameters': parameters,
                    'result_sets': all_result_sets,
                    'result_set_count': result_set_count,
                    'exec_statement': exec_statement
                }

        except Exception as e:
            self.logger.error(f"Stored procedure execution failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'procedure_name': procedure_name,
                'parameters': parameters
            }

    def close(self):
        """Close database connections (placeholder for cleanup)."""
        self.logger.info("MCP Database Tool closed")


# Global instance for easy access
mcp_database = None

def get_mcp_database(connection_name: str = 'Enterprise_Database') -> MCPDatabaseTool:
    """Get or create MCP database tool instance."""
    global mcp_database
    if mcp_database is None:
        mcp_database = MCPDatabaseTool(connection_name)
    return mcp_database
