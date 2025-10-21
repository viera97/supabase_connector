"""
Tests for conversation history functionality
"""

import os
import sys
import pytest
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from supabase_connector.conversation import (
    get_conversation_history,
    add_conversation_history,
    get_conversation_by_session,
    delete_conversation_history
)


class TestConversationFunctions:
    """Test cases for conversation history functions."""

    @patch('supabase_connector.conversation.get_global_connector')
    def test_get_conversation_history_success(self, mock_get_connector):
        """Test successful retrieval of conversation history."""
        mock_connector = Mock()
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [{'id': 1, 'message': 'test'}]
        
        mock_client.table.return_value.select.return_value.execute.return_value = mock_response
        mock_connector.get_client.return_value = mock_client
        mock_get_connector.return_value = mock_connector
        
        result = get_conversation_history()
        
        assert result == [{'id': 1, 'message': 'test'}]
        mock_client.table.assert_called_with('conversation_history')

    @patch('supabase_connector.conversation.get_global_connector')
    def test_get_conversation_history_failure(self, mock_get_connector):
        """Test failed retrieval of conversation history."""
        mock_connector = Mock()
        mock_client = Mock()
        mock_client.table.side_effect = Exception("Database error")
        mock_connector.get_client.return_value = mock_client
        mock_get_connector.return_value = mock_connector
        
        with pytest.raises(RuntimeError, match="Failed to retrieve conversation history"):
            get_conversation_history()

    @patch('supabase_connector.conversation.get_global_connector')
    def test_add_conversation_history_success(self, mock_get_connector):
        """Test successful addition of conversation history."""
        mock_connector = Mock()
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [{'id': 1}]
        
        mock_client.table.return_value.insert.return_value.execute.return_value = mock_response
        mock_connector.get_client.return_value = mock_client
        mock_get_connector.return_value = mock_connector
        
        message = {'type': 'human', 'content': 'test'}
        result = add_conversation_history('session_123', message)
        
        assert result == [{'id': 1}]

    def test_add_conversation_history_invalid_session(self):
        """Test adding conversation history with invalid session ID."""
        with pytest.raises(ValueError, match="session_id cannot be empty"):
            add_conversation_history('', {'message': 'test'})

    def test_add_conversation_history_invalid_message(self):
        """Test adding conversation history with invalid message."""
        with pytest.raises(ValueError, match="message must be a dictionary"):
            add_conversation_history('session_123', 'not a dict')

    @patch('supabase_connector.conversation.get_global_connector')
    def test_get_conversation_by_session_success(self, mock_get_connector):
        """Test successful retrieval of conversation by session."""
        mock_connector = Mock()
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [{'session_id': 'test_session'}]
        
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response
        mock_connector.get_client.return_value = mock_client
        mock_get_connector.return_value = mock_connector
        
        result = get_conversation_by_session('test_session')
        
        assert result == [{'session_id': 'test_session'}]

    def test_get_conversation_by_session_invalid_session(self):
        """Test getting conversation with invalid session ID."""
        with pytest.raises(ValueError, match="session_id cannot be empty"):
            get_conversation_by_session('')

    @patch('supabase_connector.conversation.get_global_connector')
    def test_delete_conversation_history_success(self, mock_get_connector):
        """Test successful deletion of conversation history."""
        mock_connector = Mock()
        mock_client = Mock()
        
        mock_client.table.return_value.delete.return_value.eq.return_value.execute.return_value = None
        mock_connector.get_client.return_value = mock_client
        mock_get_connector.return_value = mock_connector
        
        result = delete_conversation_history('test_session')
        
        assert result is True

    def test_delete_conversation_history_invalid_session(self):
        """Test deleting conversation with invalid session ID."""
        with pytest.raises(ValueError, match="session_id cannot be empty"):
            delete_conversation_history('')