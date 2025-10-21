#!/usr/bin/env python3
"""
Advanced Usage Example

This example demonstrates advanced features like session management,
custom configurations, and error handling.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from supabase_connector import SupabaseConnector
from supabase_connector.conversation import (
    get_conversation_by_session, 
    delete_conversation_history,
    add_conversation_history
)
from supabase_connector.utils import check_table_exists, list_available_tables

def demonstrate_session_management():
    """Show how to manage conversations by session."""
    
    print("📋 Session Management Example")
    print("-" * 40)
    
    session_id = "advanced_example_session"
    
    try:
        # Add multiple messages to a session
        messages = [
            {
                "type": "human",
                "content": "Hello, I need help with my account.",
                "timestamp": datetime.now().isoformat()
            },
            {
                "type": "assistant", 
                "content": "I'd be happy to help you with your account. What specific issue are you having?",
                "timestamp": datetime.now().isoformat()
            },
            {
                "type": "human",
                "content": "I can't log in to my dashboard.",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        print(f"➕ Adding {len(messages)} messages to session '{session_id}'...")
        for i, message in enumerate(messages, 1):
            add_conversation_history(session_id, message)
            print(f"   Added message {i}")
        
        # Retrieve session conversations
        print(f"\n📖 Retrieving conversations for session '{session_id}'...")
        session_conversations = get_conversation_by_session(session_id)
        print(f"   Found {len(session_conversations)} messages")
        
        # Display the conversation
        print("\n💬 Conversation:")
        for i, conv in enumerate(session_conversations[-3:], 1):  # Show last 3
            message = conv.get('message', {})
            msg_type = message.get('type', 'unknown')
            content = message.get('content', 'No content')[:60]
            print(f"   {i}. [{msg_type.upper()}] {content}...")
        
        # Clean up - delete the test session
        print(f"\n🗑️  Cleaning up test session...")
        delete_conversation_history(session_id)
        print("   Session deleted successfully")
        
    except Exception as e:
        print(f"❌ Session management failed: {e}")

def demonstrate_custom_connector():
    """Show how to use custom connector configurations."""
    
    print("\n🔧 Custom Connector Configuration")
    print("-" * 40)
    
    try:
        # Create connector with explicit credentials
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_ANON_KEY')
        
        if not url or not key:
            print("⚠️  Skipping custom connector demo - missing credentials")
            return
        
        print("🔧 Creating custom connector...")
        custom_connector = SupabaseConnector(url=url, key=key)
        
        # Test the custom connector
        print("🔍 Testing custom connector...")
        if custom_connector.test_connection():
            print("✅ Custom connector working!")
            
            # Get the underlying client for advanced operations
            client = custom_connector.get_client()
            print(f"✅ Got client instance: {type(client).__name__}")
        else:
            print("❌ Custom connector test failed")
            
    except Exception as e:
        print(f"❌ Custom connector demo failed: {e}")

def demonstrate_database_utilities():
    """Show how to use database utility functions."""
    
    print("\n🛠️  Database Utilities")
    print("-" * 40)
    
    try:
        # Check if conversation_history table exists
        print("🔍 Checking if conversation_history table exists...")
        if check_table_exists("conversation_history"):
            print("✅ conversation_history table exists!")
        else:
            print("❌ conversation_history table not found")
        
        # List available tables
        print("\n📋 Discovering available tables...")
        tables = list_available_tables()
        if tables:
            print(f"✅ Found {len(tables)} accessible tables:")
            for table in tables:
                print(f"   - {table}")
        else:
            print("⚠️  No accessible tables found")
        
        # Check some other common tables
        common_tables = ['users', 'profiles', 'messages', 'sessions']
        print(f"\n🔍 Checking for common tables...")
        for table in common_tables:
            exists = check_table_exists(table)
            status = "✅ EXISTS" if exists else "❌ NOT FOUND"
            print(f"   {table}: {status}")
            
    except Exception as e:
        print(f"❌ Database utilities demo failed: {e}")

def demonstrate_error_handling():
    """Show proper error handling patterns."""
    
    print("\n⚠️  Error Handling Examples")
    print("-" * 40)
    
    # Example 1: Invalid session ID
    try:
        print("🧪 Testing with empty session ID...")
        add_conversation_history("", {"content": "test"})
    except ValueError as e:
        print(f"✅ Caught expected ValueError: {e}")
    
    # Example 2: Invalid message format
    try:
        print("🧪 Testing with invalid message format...")
        add_conversation_history("test_session", "not a dict")
    except ValueError as e:
        print(f"✅ Caught expected ValueError: {e}")
    
    # Example 3: Handling database errors gracefully
    try:
        print("🧪 Testing graceful error handling...")
        # This might fail if table doesn't exist, but we handle it gracefully
        from supabase_connector.conversation import get_conversation_history
        conversations = get_conversation_history()
        print(f"✅ Success: Found {len(conversations)} conversations")
    except Exception as e:
        print(f"⚠️  Handled database error gracefully: {type(e).__name__}")

def main():
    """Run the advanced usage example."""
    
    # Load environment variables
    load_dotenv()
    
    print("🚀 Supabase Connector - Advanced Usage Example")
    print("=" * 60)
    
    # Check basic connectivity first
    try:
        connector = SupabaseConnector()
        if not connector.test_connection():
            print("❌ Basic connection failed. Please check your configuration.")
            return 1
    except Exception as e:
        print(f"❌ Failed to initialize connector: {e}")
        return 1
    
    # Run demonstrations
    demonstrate_session_management()
    demonstrate_custom_connector()
    demonstrate_database_utilities()
    demonstrate_error_handling()
    
    print("\n🎉 Advanced usage example completed!")
    print("\n💡 Next steps:")
    print("   - Explore the API documentation in docs/")
    print("   - Check out the test files for more examples")
    print("   - Build your own application using these patterns")
    
    return 0

if __name__ == "__main__":
    exit(main())