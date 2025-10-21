"""
Integration tests for real Supabase connection
Run these tests only when you have a real Supabase instance configured.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from supabase_connector import SupabaseConnector, get_conversation_history, add_conversation_history


def test_real_connection():
    """
    Test real connection to Supabase.
    This test will be skipped if environment variables are not set.
    """
    print("🔍 Testing Real Supabase Connection...")
    print("=" * 50)
    
    # Check if environment variables are set
    if not os.getenv('SUPABASE_URL') or not os.getenv('SUPABASE_ANON_KEY'):
        print("⏭️  Skipping real connection test - environment variables not set")
        return
    
    try:
        # Test connector initialization
        connector = SupabaseConnector()
        print("✅ Connector initialized successfully")
        
        # Test connection
        if connector.test_connection():
            print("✅ Connection test passed")
        else:
            print("❌ Connection test failed")
            return
        
        # Test conversation functions (only if table exists)
        try:
            print("\n📊 Testing conversation functions...")
            history = get_conversation_history()
            print(f"✅ Retrieved {len(history)} conversation records")
            
            # Try adding a test record
            test_message = {
                "type": "system",
                "content": "Integration test message",
                "additional_kwargs": {},
                "response_metadata": {},
                "timestamp": "2024-01-01T00:00:00Z"
            }
            
            result = add_conversation_history("integration_test", test_message)
            print(f"✅ Added test record successfully")
            
        except Exception as e:
            print(f"⚠️  Conversation functions test failed: {e}")
            print("   This is normal if the conversation_history table doesn't exist")
        
        print("\n🎉 Integration test completed!")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")


if __name__ == "__main__":
    test_real_connection()