"""
Supabase Connector Package

A Python package for connecting and interacting with Supabase databases.
Provides easy-to-use functions for managing conversation history and other operations.
"""

__version__ = "0.1.0"
__author__ = "Dayron Viera Quintero"
__email__ = "d.viera1997@gmail.com"

from .client import SupabaseConnector
from .conversation import get_conversation_history, add_conversation_history
from .services import (
    get_services,
    get_service_categories,
    get_services_summary
)
from .info import (
    get_info,
    get_info_name,
    get_info_phone,
    get_info_address,
    get_info_email,
    get_info_description,
)

__all__ = [
    "SupabaseConnector",
    "get_conversation_history", 
    "add_conversation_history",
    "get_services",
    "get_service_categories",
    "get_services_summary",
    "get_info",
    "get_info_name",
    "get_info_phone", 
    "get_info_address",
    "get_info_email",
    "get_info_description",
]