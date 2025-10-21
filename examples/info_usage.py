#!/usr/bin/env python3
"""
Info Management Usage Example

This example demonstrates how to use the info management functions
to retrieve information from the public.info table.

The info table contains a single row with company/contact information.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path for development
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Now import our functions
from supabase_connector import (
    get_info,
    get_info_name,
    get_info_phone,
    get_info_address,
    get_info_email,
    get_info_description,
    get_info_created_at,
    get_info_id
)


def main():
    """Demonstrate info management functionality."""
    
    print("🏢 Info Management Demo")
    print("=" * 50)
    
    # 1. Get complete info record
    print("\n📋 Complete Info Record:")
    info = get_info()
    if info:
        for key, value in info.items():
            print(f"  {key}: {value}")
    else:
        print("  No info record found")
    
    print("\n" + "=" * 50)
    
    # 2. Get individual fields
    print("\n🔍 Individual Fields:")
    
    # Name
    name = get_info_name()
    print(f"  Name: {name}")
    
    # Phone
    phone = get_info_phone()
    print(f"  Phone: {phone}")
    
    # Address
    address = get_info_address()
    print(f"  Address: {address}")
    
    # Email
    email = get_info_email()
    print(f"  Email: {email}")
    
    # Description
    description = get_info_description()
    print(f"  Description: {description}")
    
    # Created At
    created_at = get_info_created_at()
    print(f"  Created At: {created_at}")
    
    # ID
    info_id = get_info_id()
    print(f"  ID: {info_id}")
    
    print("\n" + "=" * 50)
    
    # 3. Practical usage examples
    print("\n💡 Practical Usage Examples:")
    
    # Contact information display
    if name and email:
        print(f"  Contact: {name} ({email})")
    
    # Address formatting
    if address:
        print(f"  Visit us at: {address}")
    
    # Phone formatting
    if phone:
        print(f"  Call us: {phone}")
    
    # Description display
    if description:
        print(f"  About: {description}")


if __name__ == "__main__":
    # Make sure we have environment setup
    env_file = project_root / ".env"
    if not env_file.exists():
        print("❌ Error: .env file not found!")
        print("Please create a .env file with your Supabase credentials.")
        print("See README.md for setup instructions.")
        sys.exit(1)
    
    try:
        main()
    except Exception as e:
        print(f"❌ Error running info demo: {e}")
        print("\nTroubleshooting:")
        print("1. Check your .env file has correct Supabase credentials")
        print("2. Ensure the 'info' table exists in your 'public' schema")
        print("3. Verify your user has SELECT permissions on public.info")
        sys.exit(1)