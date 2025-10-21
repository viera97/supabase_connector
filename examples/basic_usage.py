#!/usr/bin/env python3
"""
Basic Usage Example

This example shows how to use the Supabase Connector for basic operations.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from supabase_connector import SupabaseConnector, get_conversation_history, add_conversation_history

def main():
    """Demonstrate basic usage of the Supabase Connector."""
    
    # Load environment variables
    load_dotenv()
    
    print("🚀 Supabase Connector - Basic Usage Example")
    print("=" * 50)
    
    try:
        # 1. Initialize the connector
        print("1️⃣ Initializing Supabase Connector...")
        connector = SupabaseConnector()
        print("✅ Connector initialized successfully!")
        
        # 2. Test the connection
        print("\n2️⃣ Testing connection...")
        if connector.test_connection():
            print("✅ Connection successful!")
        else:
            print("❌ Connection failed!")
            return
        
        # 3. Get conversation history
        print("\n3️⃣ Retrieving conversation history...")
        try:
            conversations = get_conversation_history()
            print(f"✅ Found {len(conversations)} conversation records")
            
            # Show sample data if available
            if conversations:
                print("\n📝 Sample conversation record:")
                sample = conversations[0]
                for key, value in sample.items():
                    if isinstance(value, str) and len(value) > 50:
                        value = value[:50] + "..."
                    print(f"   {key}: {value}")
            
        except Exception as e:
            print(f"⚠️  Could not retrieve conversations: {e}")
            print("   This is normal if the conversation_history table doesn't exist yet.")
        
        # 4. Add a new conversation
        print("\n4️⃣ Adding a test conversation...")
        try:
            test_message = {
                "type": "human",
                "content": "Hello! This is a test message from the basic usage example.",
                "additional_kwargs": {},
                "response_metadata": {},
                "timestamp": "2024-01-01T12:00:00Z"
            }
            
            result = add_conversation_history("example_session_001", test_message)
            print(f"✅ Added conversation successfully! Records returned: {len(result)}")
            
        except Exception as e:
            print(f"⚠️  Could not add conversation: {e}")
            print("   Make sure the conversation_history table exists in your database.")
        
        print("\n🎉 Basic usage example completed!")
        
    except Exception as e:
        print(f"❌ Example failed: {e}")
        print("\n💡 Make sure you have:")
        print("   - Created a .env file with SUPABASE_URL and SUPABASE_ANON_KEY")
        print("   - Created the conversation_history table in your Supabase database")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())