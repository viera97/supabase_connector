"""
Tests for the Supabase client functionality
"""

import os
import sys
import pytest
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from supabase_connector.client import SupabaseConnector


class TestSupabaseConnector:
    """Test cases for SupabaseConnector class."""

    def test_initialization_with_credentials(self):
        """Test connector initialization with provided credentials."""
        with patch('supabase_connector.client.create_client') as mock_create:
            mock_client = Mock()
            mock_create.return_value = mock_client
            
            connector = SupabaseConnector(
                url="test_url",
                key="test_key"
            )
            
            assert connector.url == "test_url"
            assert connector.key == "test_key"
            mock_create.assert_called_once_with("test_url", "test_key")

    def test_initialization_without_credentials_fails(self):
        """Test that initialization fails without credentials."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Supabase credentials not found"):
                SupabaseConnector()

    @patch.dict(os.environ, {
        'SUPABASE_URL': 'env_url',
        'SUPABASE_ANON_KEY': 'env_key'
    })
    def test_initialization_from_environment(self):
        """Test connector initialization from environment variables."""
        with patch('supabase_connector.client.create_client') as mock_create:
            mock_client = Mock()
            mock_create.return_value = mock_client
            
            connector = SupabaseConnector()
            
            assert connector.url == "env_url"
            assert connector.key == "env_key"

    def test_get_client(self):
        """Test getting the client instance."""
        with patch('supabase_connector.client.create_client') as mock_create:
            mock_client = Mock()
            mock_create.return_value = mock_client
            
            connector = SupabaseConnector(url="test", key="test")
            client = connector.get_client()
            
            assert client == mock_client

    def test_test_connection_success(self):
        """Test successful connection test."""
        with patch('supabase_connector.client.create_client') as mock_create:
            mock_client = Mock()
            mock_client.auth.get_user.return_value = True
            mock_create.return_value = mock_client
            
            connector = SupabaseConnector(url="test", key="test")
            result = connector.test_connection()
            
            assert result is True

    def test_test_connection_failure(self):
        """Test failed connection test."""
        with patch('supabase_connector.client.create_client') as mock_create:
            mock_client = Mock()
            mock_client.auth.get_user.side_effect = Exception("Connection failed")
            mock_create.return_value = mock_client
            
            connector = SupabaseConnector(url="test", key="test")
            result = connector.test_connection()
            
            assert result is False