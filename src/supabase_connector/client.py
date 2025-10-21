"""
Supabase Client Configuration and Initialization
"""

import os
from typing import Optional
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()


class SupabaseConnector:
    """
    A wrapper class for Supabase client with configuration management.
    """
    
    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        """
        Initialize the Supabase connector.
        
        Parameters
        ----------
        url : str, optional
            Supabase URL. If not provided, will look for SUPABASE_URL environment variable.
        key : str, optional
            Supabase anonymous key. If not provided, will look for SUPABASE_ANON_KEY environment variable.
            
        Raises
        ------
        ValueError
            If credentials are not provided and not found in environment variables.
        """
        self.url = url or os.getenv('SUPABASE_URL')
        self.key = key or os.getenv('SUPABASE_ANON_KEY')
        
        if not self.url or not self.key:
            raise ValueError(
                "Supabase credentials not found. Please provide url and key parameters "
                "or set SUPABASE_URL and SUPABASE_ANON_KEY environment variables."
            )
        
        self.client: Client = create_client(self.url, self.key)
    
    def get_client(self) -> Client:
        """
        Get the Supabase client instance.
        
        Returns
        -------
        Client
            The Supabase client instance.
        """
        return self.client
    
    def test_connection(self) -> bool:
        """
        Test the connection to Supabase.
        
        Returns
        -------
        bool
            True if connection is successful, False otherwise.
        """
        try:
            # Try to get current user to test connection
            self.client.auth.get_user()
            return True
        except Exception:
            return False


# Create a global instance for backwards compatibility
_global_connector: Optional[SupabaseConnector] = None

def get_global_connector() -> SupabaseConnector:
    """
    Get or create a global Supabase connector instance.
    
    Returns
    -------
    SupabaseConnector
        The global connector instance.
    """
    global _global_connector
    if _global_connector is None:
        _global_connector = SupabaseConnector()
    return _global_connector