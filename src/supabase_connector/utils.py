"""
Database utilities and helper functions
"""

from typing import List, Dict, Any, Optional
from .client import get_global_connector


def check_table_exists(table_name: str, schema: str = 'public') -> bool:
    """
    Check if a table exists in the database.
    
    Parameters
    ----------
    table_name : str
        Name of the table to check.
    schema : str, optional
        Schema name, defaults to 'public'.
        
    Returns
    -------
    bool
        True if table exists, False otherwise.
    """
    try:
        connector = get_global_connector()
        client = connector.get_client()
        
        # Try a simple query to check if table exists
        client.table(table_name).select('*').limit(1).execute()
        return True
    except Exception:
        return False


def get_table_info(table_name: str) -> Optional[Dict[str, Any]]:
    """
    Get basic information about a table.
    
    Parameters
    ----------
    table_name : str
        Name of the table.
        
    Returns
    -------
    Optional[Dict[str, Any]]
        Dictionary with table information or None if table doesn't exist.
    """
    try:
        connector = get_global_connector()
        client = connector.get_client()
        
        # Get a sample record to understand table structure
        response = client.table(table_name).select('*').limit(1).execute()
        
        info = {
            'table_name': table_name,
            'exists': True,
            'sample_record': response.data[0] if response.data else None,
            'record_count': len(response.data)
        }
        
        return info
    except Exception:
        return None


def list_available_tables() -> List[str]:
    """
    Attempt to discover available tables by trying common table names.
    
    Returns
    -------
    List[str]
        List of table names that exist and are accessible.
    """
    common_tables = [
        'conversation_history',
        'users',
        'profiles',
        'messages',
        'chat',
        'sessions',
        'logs',
        'settings',
        'test'
    ]
    
    available_tables = []
    
    for table in common_tables:
        if check_table_exists(table):
            available_tables.append(table)
    
    return available_tables


def create_conversation_history_table() -> bool:
    """
    Create the conversation_history table if it doesn't exist.
    Note: This requires appropriate database permissions.
    
    Returns
    -------
    bool
        True if table was created or already exists, False otherwise.
    """
    # Note: This would typically require database admin permissions
    # and would use SQL DDL commands. For now, we'll just check if it exists.
    return check_table_exists('conversation_history')