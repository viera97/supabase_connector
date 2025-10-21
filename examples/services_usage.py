#!/usr/bin/env python3
"""
Services Example Script

Demonstrates how to use the services functions to interact with the services table.
"""

import sys
import os
from dotenv import load_dotenv

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from supabase_connector import (
    SupabaseConnector,
    get_services,
    get_service_categories,
    get_services_summary
)

def main():
    """Demonstrate services functionality."""
    
    # Load environment variables
    load_dotenv()
    
    print("🛠️ Supabase Connector - Services Example")
    print("=" * 50)
    
    try:
        # 1. Test connection
        print("1️⃣ Testing connection...")
        connector = SupabaseConnector()
        
        if not connector.test_connection():
            print("❌ Connection failed! Check your .env configuration")
            return 1
        
        print("✅ Connection successful!")
        
        # 2. Get all services
        print("\n2️⃣ Getting all services...")
        all_services = []
        try:
            all_services = get_services()
            print(f"✅ Found {len(all_services)} services total")
            
            if all_services:
                print("\n📋 First few services:")
                for service in all_services[:3]:
                    print(f"   • {service['name']} ({service['category']}) - ${service.get('price', 'N/A')}")
        
        except Exception as e:
            print(f"⚠️  Could not retrieve all services: {e}")
        
        # 3. Get active services only
        print("\n3️⃣ Getting active services...")
        try:
            active_services = get_services(is_active=True, limit=5)
            print(f"✅ Found {len(active_services)} active services (showing max 5)")
            
            for service in active_services:
                duration = service.get('duration_minutes', 'N/A')
                print(f"   • {service['name']}: {duration} min, ${service.get('price', 'N/A')}")
        
        except Exception as e:
            print(f"⚠️  Could not retrieve active services: {e}")
        
        # 4. Get service categories
        print("\n4️⃣ Getting service categories...")
        try:
            categories = get_service_categories()
            print(f"✅ Found {len(categories)} categories:")
            for category in categories:
                print(f"   📂 {category}")
        
        except Exception as e:
            print(f"⚠️  Could not retrieve categories: {e}")
            categories = []
        
        # 5. Search by category (if we have categories)
        if categories:
            print(f"\n5️⃣ Getting services in '{categories[0]}' category...")
            try:
                category_services = get_services(category=categories[0])
                print(f"✅ Found {len(category_services)} services in '{categories[0]}'")
                
                for service in category_services[:3]:
                    print(f"   • {service['name']}: {service.get('description', 'No description')[:50]}...")
            
            except Exception as e:
                print(f"⚠️  Could not retrieve services by category: {e}")
        
        # 6. Search by name
        print("\n6️⃣ Searching services by name...")
        search_terms = ["massage", "facial", "therapy", "consultation"]
        
        for term in search_terms:
            try:
                search_results = get_services(name=term)
                if search_results:
                    print(f"✅ Found {len(search_results)} services containing '{term}':")
                    for service in search_results[:2]:
                        print(f"   • {service['name']}")
                    break
            except Exception as e:
                print(f"⚠️  Search for '{term}' failed: {e}")
        
        # 7. Get specific service by ID
        print("\n7️⃣ Getting specific service by ID...")
        if all_services:
            service_id = all_services[0]['id']
            try:
                specific_services = get_services(service_id=service_id)
                if specific_services:
                    specific_service = specific_services[0]  # get_services returns a list
                    print(f"✅ Service ID {service_id}:")
                    print(f"   📛 Name: {specific_service['name']}")
                    print(f"   📂 Category: {specific_service['category']}")
                    print(f"   💰 Price: ${specific_service.get('price', 'N/A')}")
                    print(f"   ⏰ Duration: {specific_service.get('duration_minutes', 'N/A')} minutes")
                    print(f"   📝 Description: {specific_service.get('description', 'No description')[:100]}...")
                    print(f"   ✅ Active: {specific_service.get('is_active', False)}")
                else:
                    print(f"❌ Service ID {service_id} not found")
            except Exception as e:
                print(f"⚠️  Could not retrieve service by ID: {e}")
        
        # 8. Get services summary
        print("\n8️⃣ Getting services summary...")
        try:
            summary = get_services_summary()
            print("✅ Services Summary:")
            print(f"   📊 Total Services: {summary['total_services']}")
            print(f"   🟢 Active Services: {summary['active_services']}")
            print(f"   🔴 Inactive Services: {summary['inactive_services']}")
            print(f"   📂 Total Categories: {summary['total_categories']}")
            print(f"   💰 Average Price: ${summary['average_price']:.2f}")
            print(f"   ⏰ Average Duration: {summary['average_duration']:.1f} minutes")
            
            if summary['services_by_category']:
                print("   📂 Services by Category:")
                for category, count in summary['services_by_category'].items():
                    print(f"      • {category}: {count} services")
        
        except Exception as e:
            print(f"⚠️  Could not generate summary: {e}")
        
        print("\n🎉 Services example completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ Example failed: {e}")
        print("\n💡 Make sure you have:")
        print("   - Created a .env file with SUPABASE_URL and SUPABASE_ANON_KEY")
        print("   - A 'services' table exists in the 'public' schema")
        print("   - The table has the expected columns")
        return 1

if __name__ == "__main__":
    exit(main())