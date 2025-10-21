"""
Conversation History Management Functions
"""

from typing import List, Dict, Any
from .client import get_global_connector


def get_conversation_history() -> List[Dict[str, Any]]:
    """
    Retrieves all conversation history records from Supabase.

    Returns
    -------
    List[Dict[str, Any]]
        A list of conversation history records.

    Raises
    -------
    RuntimeError
        If the Supabase client is not initialized or the query fails.
    """
    try:
        connector = get_global_connector()
        client = connector.get_client()
        
        # Query the conversation_history table
        response = client.schema("chatbot").table('conversation_history').select('*').execute()
        
        return response.data
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve conversation history: {e}")


def add_conversation_history(session_id: str, message: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Adds a new conversation history record to Supabase.

    Parameters
    ----------
    session_id : str
        The ID of the session.
    message : Dict[str, Any]
        The message to be added to the history.

    Returns
    -------
    List[Dict[str, Any]]
        The data returned by the Supabase client.

    Raises
    -------
    RuntimeError
        If the Supabase client is not initialized or the insert fails.
    ValueError
        If session_id is empty or message is invalid.
    """
    if not session_id or not session_id.strip():
        raise ValueError("session_id cannot be empty")
    
    if not isinstance(message, dict):
        raise ValueError("message must be a dictionary")
    
    try:
        connector = get_global_connector()
        client = connector.get_client()
        
        data = {
            "session_id": session_id.strip(),
            "message": message,
        }
        
        response = client.table('conversation_history').insert(data).execute()
        return response.data
    except Exception as e:
        raise RuntimeError(f"Failed to add conversation history: {e}")


def get_conversation_by_session(session_id: str) -> List[Dict[str, Any]]:
    """
    Retrieves conversation history for a specific session.

    Parameters
    ----------
    session_id : str
        The ID of the session.

    Returns
    -------
    List[Dict[str, Any]]
        A list of conversation records for the specified session.

    Raises
    -------
    RuntimeError
        If the query fails.
    ValueError
        If session_id is empty.
    """
    if not session_id or not session_id.strip():
        raise ValueError("session_id cannot be empty")
    
    try:
        connector = get_global_connector()
        client = connector.get_client()
        
        response = client.table('conversation_history').select('*').eq('session_id', session_id.strip()).execute()
        return response.data
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve conversation for session {session_id}: {e}")


def delete_conversation_history(session_id: str) -> bool:
    """
    Deletes all conversation history for a specific session.

    Parameters
    ----------
    session_id : str
        The ID of the session.

    Returns
    -------
    bool
        True if deletion was successful, False otherwise.

    Raises
    -------
    ValueError
        If session_id is empty.
    """
    if not session_id or not session_id.strip():
        raise ValueError("session_id cannot be empty")
    
    try:
        connector = get_global_connector()
        client = connector.get_client()
        
        client.table('conversation_history').delete().eq('session_id', session_id.strip()).execute()
        return True
    except Exception as e:
        raise RuntimeError(f"Failed to delete conversation history for session {session_id}: {e}")