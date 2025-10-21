"""
Test suite for Supabase Connector
"""

import pytest
import os
from unittest.mock import Mock, patch
from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv()

# Add src to path for importing
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from supabase_connector.client import SupabaseConnector
from supabase_connector.conversation import (
    get_conversation_history,
    add_conversation_history,
    get_conversation_by_session
)