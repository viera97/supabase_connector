"""
Info Management Functions

Functions for managing the single row in the public.info table.

Table schema:
- id: Primary key
- name: Contact name
- phone: Phone number  
- address: Physical address
- created_at: Creation timestamp
- description: General description
- email: Email address

Since this table contains only one row, these functions retrieve
that single record and provide easy access to individual fields.
"""

from typing import Dict, Any, Optional
from .client import get_global_connector


def get_info() -> Optional[Dict[str, Any]]:
    """
    Retrieve the complete information record from the public.info table.
    
    Returns
    -------
    dict or None
        Dictionary containing all info fields, or None if no data found.
        
    Example
    -------
    >>> info = get_info()
    >>> print(info)
    {
        'id': 1,
        'name': 'COGI',
        'phone': '+1234567890',
        'address': '123 Main St',
        'created_at': '2024-01-01T00:00:00+00:00',
        'description': 'Company information',
        'email': 'contact@cogi.com'
    }
    """
    try:
        connector = get_global_connector()
        response = connector.client.table("info").select("*").execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
        
    except Exception as e:
        print(f"Error retrieving info: {e}")
        return None


def get_info_name() -> Optional[str]:
    """
    Get the name field from the info table.
    
    Returns
    -------
    str or None
        The name value, or None if not found.
    """
    try:
        info = get_info()
        return info.get('name') if info else None
    except Exception as e:
        print(f"Error retrieving info name: {e}")
        return None


def get_info_phone() -> Optional[str]:
    """
    Get the phone field from the info table.
    
    Returns
    -------
    str or None
        The phone value, or None if not found.
    """
    try:
        info = get_info()
        return info.get('phone') if info else None
    except Exception as e:
        print(f"Error retrieving info phone: {e}")
        return None


def get_info_address() -> Optional[str]:
    """
    Get the address field from the info table.
    
    Returns
    -------
    str or None
        The address value, or None if not found.
    """
    try:
        info = get_info()
        return info.get('address') if info else None
    except Exception as e:
        print(f"Error retrieving info address: {e}")
        return None


def get_info_email() -> Optional[str]:
    """
    Get the email field from the info table.
    
    Returns
    -------
    str or None
        The email value, or None if not found.
    """
    try:
        info = get_info()
        return info.get('email') if info else None
    except Exception as e:
        print(f"Error retrieving info email: {e}")
        return None


def get_info_description() -> Optional[str]:
    """
    Get the description field from the info table.
    
    Returns
    -------
    str or None
        The description value, or None if not found.
    """
    try:
        info = get_info()
        return info.get('description') if info else None
    except Exception as e:
        print(f"Error retrieving info description: {e}")
        return None


def get_info_created_at() -> Optional[str]:
    """
    Get the created_at field from the info table.
    
    Returns
    -------
    str or None
        The created_at timestamp, or None if not found.
    """
    try:
        info = get_info()
        return info.get('created_at') if info else None
    except Exception as e:
        print(f"Error retrieving info created_at: {e}")
        return None


def get_info_id() -> Optional[int]:
    """
    Get the id field from the info table.
    
    Returns
    -------
    int or None
        The id value, or None if not found.
    """
    try:
        info = get_info()
        return info.get('id') if info else None
    except Exception as e:
        print(f"Error retrieving info id: {e}")
        return None