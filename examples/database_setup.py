#!/usr/bin/env python3
"""
Database Setup Example

This script helps you set up the required database tables and verify
your Supabase configuration.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from supabase_connector.client import SupabaseConnector
from supabase_connector.utils import check_table_exists, list_available_tables

def print_sql_schema():
    """Print the SQL commands needed to create the required tables."""
    
    print("📄 Required Database Schema")
    print("=" * 50)
    print()
    print("Copy and paste this SQL into your Supabase SQL editor:")
    print()
    print("```sql")
    print("-- Create conversation_history table")
    print("CREATE TABLE conversation_history (")
    print("  id BIGSERIAL PRIMARY KEY,")
    print("  session_id TEXT NOT NULL,")
    print("  message JSONB NOT NULL,")
    print("  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()")
    print(");")
    print()
    print("-- Add indexes for better performance")
    print("CREATE INDEX idx_conversation_history_session_id")
    print("ON conversation_history(session_id);")
    print()
    print("CREATE INDEX idx_conversation_history_created_at")
    print("ON conversation_history(created_at);")
    print()
    print("-- Enable Row Level Security (optional but recommended)")
    print("ALTER TABLE conversation_history ENABLE ROW LEVEL SECURITY;")
    print()
    print("-- Create a policy to allow authenticated users to access their data")
    print("CREATE POLICY \"Users can access their own conversations\"")
    print("ON conversation_history")
    print("FOR ALL")
    print("USING (true);  -- Adjust this based on your security needs")
    print("```")
    print()

def check_database_setup():
    """Check the current database setup and provide guidance."""
    
    print("🔍 Checking Database Setup")
    print("=" * 50)
    
    try:
        # Initialize connector
        connector = SupabaseConnector()
        
        # Test connection
        print("1️⃣ Testing connection...")
        if not connector.test_connection():
            print("❌ Connection failed!")
            print("   Please check your SUPABASE_URL and SUPABASE_ANON_KEY")
            return False
        
        print("✅ Connection successful!")
        
        # Check for required table
        print("\n2️⃣ Checking for conversation_history table...")
        if check_table_exists("conversation_history"):
            print("✅ conversation_history table exists!")
            
            # Test basic operations
            print("\n3️⃣ Testing basic operations...")
            try:
                client = connector.get_client()
                
                # Test select
                response = client.table('conversation_history').select('*').limit(1).execute()
                print(f"✅ SELECT operation works! (found {len(response.data)} records)")
                
                # Test insert (we'll add and immediately delete)
                test_data = {
                    "session_id": "setup_test_session",
                    "message": {"type": "system", "content": "Setup test"}
                }
                
                insert_response = client.table('conversation_history').insert(test_data).execute()
                print("✅ INSERT operation works!")
                
                # Clean up test data
                client.table('conversation_history').delete().eq('session_id', 'setup_test_session').execute()
                print("✅ DELETE operation works!")
                
                print("\n🎉 Database setup is complete and working!")
                return True
                
            except Exception as e:
                print(f"⚠️  Basic operations test failed: {e}")
                print("   The table exists but there might be permission issues.")
                return False
        
        else:
            print("❌ conversation_history table not found!")
            
            # Show available tables
            print("\n📋 Available tables:")
            tables = list_available_tables()
            if tables:
                for table in tables:
                    print(f"   - {table}")
            else:
                print("   No accessible tables found")
            
            print("\n💡 You need to create the conversation_history table.")
            print("   See the SQL schema above.")
            return False
            
    except Exception as e:
        print(f"❌ Database setup check failed: {e}")
        return False

def interactive_setup():
    """Interactive setup wizard."""
    
    print("🧙 Interactive Setup Wizard")
    print("=" * 50)
    
    # Check environment variables
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_ANON_KEY')
    
    if not url:
        print("❌ SUPABASE_URL not found in environment variables")
        print("   Please add it to your .env file")
        return
    
    if not key:
        print("❌ SUPABASE_ANON_KEY not found in environment variables")
        print("   Please add it to your .env file")
        return
    
    print(f"✅ Found SUPABASE_URL: {url}")
    print(f"✅ Found SUPABASE_ANON_KEY: {key[:20]}...")
    
    # Test connection
    try:
        connector = SupabaseConnector()
        if connector.test_connection():
            print("✅ Connection to Supabase successful!")
        else:
            print("❌ Connection to Supabase failed!")
            print("   Please check your credentials and internet connection")
            return
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return
    
    # Check table setup
    if check_table_exists("conversation_history"):
        print("✅ conversation_history table is already set up!")
        print("\n🎉 Your setup is complete! You're ready to use the connector.")
    else:
        print("❌ conversation_history table not found")
        print("\n📝 Next steps:")
        print("   1. Go to your Supabase project dashboard")
        print("   2. Open the SQL Editor")
        print("   3. Run the SQL schema provided above")
        print("   4. Run this setup script again to verify")

def main():
    """Run the database setup example."""
    
    # Load environment variables
    load_dotenv()
    
    print("🏗️  Supabase Connector - Database Setup")
    print("=" * 60)
    
    # Print the required schema
    print_sql_schema()
    
    # Check current setup
    setup_ok = check_database_setup()
    
    if not setup_ok:
        print("\n" + "=" * 60)
        interactive_setup()
    
    print("\n📚 Additional Resources:")
    print("   - Supabase Documentation: https://supabase.com/docs")
    print("   - SQL Editor: https://app.supabase.com/project/[your-project]/sql")
    print("   - Table Editor: https://app.supabase.com/project/[your-project]/editor")
    
    return 0 if setup_ok else 1

if __name__ == "__main__":
    exit(main())