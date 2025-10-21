#!/usr/bin/env python3
"""
Tests for Info Management Functions

Tests for the info.py module functions.
"""

import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from supabase_connector.info import (
    get_info,
    get_info_name,
    get_info_phone,
    get_info_address,
    get_info_email,
    get_info_description,
    get_info_created_at,
    get_info_id
)


def test_get_info():
    """Test the get_info function."""
    print("Testing get_info()...")
    
    # Mock data
    mock_data = {
        'id': 1,
        'name': 'COGI Company',
        'phone': '+1234567890',
        'address': '123 Main Street',
        'email': 'contact@cogi.com',
        'description': 'Technology company',
        'created_at': '2024-01-01T00:00:00+00:00'
    }
    
    # Mock the connector and response
    with patch('supabase_connector.info.get_global_connector') as mock_get_connector:
        mock_connector = Mock()
        mock_response = Mock()
        mock_response.data = [mock_data]
        
        mock_connector.client.table.return_value.select.return_value.execute.return_value = mock_response
        mock_get_connector.return_value = mock_connector
        
        # Test successful retrieval
        result = get_info()
        assert result == mock_data
        print("  ✅ get_info() returns correct data")
        
        # Test empty result
        mock_response.data = []
        result = get_info()
        assert result is None
        print("  ✅ get_info() returns None when no data")


def test_individual_field_functions():
    """Test individual field retrieval functions."""
    print("\nTesting individual field functions...")
    
    mock_data = {
        'id': 1,
        'name': 'COGI Company',
        'phone': '+1234567890',
        'address': '123 Main Street',
        'email': 'contact@cogi.com',
        'description': 'Technology company',
        'created_at': '2024-01-01T00:00:00+00:00'
    }
    
    with patch('supabase_connector.info.get_info', return_value=mock_data):
        # Test each field function
        assert get_info_name() == 'COGI Company'
        print("  ✅ get_info_name() works")
        
        assert get_info_phone() == '+1234567890'
        print("  ✅ get_info_phone() works")
        
        assert get_info_address() == '123 Main Street'
        print("  ✅ get_info_address() works")
        
        assert get_info_email() == 'contact@cogi.com'
        print("  ✅ get_info_email() works")
        
        assert get_info_description() == 'Technology company'
        print("  ✅ get_info_description() works")
        
        assert get_info_created_at() == '2024-01-01T00:00:00+00:00'
        print("  ✅ get_info_created_at() works")
        
        assert get_info_id() == 1
        print("  ✅ get_info_id() works")


def test_field_functions_with_no_data():
    """Test field functions when no data is available."""
    print("\nTesting field functions with no data...")
    
    with patch('supabase_connector.info.get_info', return_value=None):
        # All functions should return None when no data
        assert get_info_name() is None
        assert get_info_phone() is None
        assert get_info_address() is None
        assert get_info_email() is None
        assert get_info_description() is None
        assert get_info_created_at() is None
        assert get_info_id() is None
        print("  ✅ All field functions return None when no data")


def test_field_functions_with_missing_fields():
    """Test field functions when some fields are missing."""
    print("\nTesting field functions with missing fields...")
    
    # Mock data with missing fields
    incomplete_data = {
        'id': 1,
        'name': 'COGI Company'
        # Missing other fields
    }
    
    with patch('supabase_connector.info.get_info', return_value=incomplete_data):
        assert get_info_name() == 'COGI Company'
        assert get_info_phone() is None
        assert get_info_address() is None
        assert get_info_email() is None
        assert get_info_id() == 1
        print("  ✅ Field functions handle missing fields correctly")


if __name__ == "__main__":
    print("🧪 Running Info Management Tests")
    print("=" * 50)
    
    try:
        test_get_info()
        test_individual_field_functions()
        test_field_functions_with_no_data()
        test_field_functions_with_missing_fields()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)