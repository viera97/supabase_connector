#!/usr/bin/env python3
"""
Quick Services Test Script

Simple script to test services functions.
"""

import sys
import os
from dotenv import load_dotenv

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_services():
    """Quick test of services functions."""
    
    load_dotenv()
    
    try:
        from supabase_connector import get_services, get_service_categories, get_services_summary
        
        print("🧪 Quick Services Test")
        print("=" * 30)
        
        # Test 1: Get all services
        print("1️⃣ Testing get_services()...")
        services = get_services()
        print(f"✅ Found {len(services)} services")
        
        # Test 2: Get categories
        print("\n2️⃣ Testing get_service_categories()...")
        categories = get_service_categories()
        print(f"✅ Found categories: {categories}")
        
        # Test 3: Filter by category
        if categories:
            print(f"\n3️⃣ Testing filter by category '{categories[0]}'...")
            category_services = get_services(category=categories[0])
            print(f"✅ Found {len(category_services)} services in '{categories[0]}'")
        
        # Test 4: Get summary
        print(f"\n4️⃣ Testing get_services_summary()...")
        summary = get_services_summary()
        print(f"✅ Summary: {summary['total_services']} total, {summary['active_services']} active")
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if test_services():
        print("\n💡 Usage examples:")
        print("  from supabase_connector import get_services")
        print("  services = get_services(category='spa', is_active=True)")
        print("  service = get_service_by_id(1)")
        print("  results = search_services_by_name('massage')")
    else:
        print("\n💡 Check your .env file and database connection")