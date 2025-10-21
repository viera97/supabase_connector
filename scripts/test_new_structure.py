#!/usr/bin/env python3
"""
Test Connection Script for New Structure

This script helps test the new package structure.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def main():
    """Test the new package structure."""
    
    load_dotenv()
    
    print("🧪 Testing New Package Structure")
    print("=" * 50)
    
    try:
        # Test imports
        print("1️⃣ Testing imports...")
        from supabase_connector import SupabaseConnector, get_conversation_history, add_conversation_history
        from supabase_connector.utils import check_table_exists, list_available_tables
        print("✅ All imports successful!")
        
        # Test connector initialization
        print("\n2️⃣ Testing connector initialization...")
        connector = SupabaseConnector()
        print("✅ Connector initialized!")
        
        # Test connection
        print("\n3️⃣ Testing connection...")
        if connector.test_connection():
            print("✅ Connection successful!")
        else:
            print("⚠️  Connection test failed (this might be normal)")
        
        # Test utility functions
        print("\n4️⃣ Testing utilities...")
        tables = list_available_tables()
        print(f"✅ Found {len(tables)} accessible tables")
        
        if check_table_exists("conversation_history"):
            print("✅ conversation_history table exists!")
            
            # Test conversation functions
            print("\n5️⃣ Testing conversation functions...")
            try:
                history = get_conversation_history()
                print(f"✅ Retrieved {len(history)} conversation records")
            except Exception as e:
                print(f"⚠️  Could not retrieve conversations: {e}")
        else:
            print("⚠️  conversation_history table not found")
        
        print("\n🎉 New package structure is working!")
        return 0
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())