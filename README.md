# Supabase Connector

A Python package for connecting and interacting with Supabase databases. This package provides easy-to-use functions for managing conversation history and other database operations.

## 🏗️ Project Structure

```
supabase_connector/
├── src/
│   └── supabase_connector/          # Main package source code
       ├── __init__.py              # Package initialization and exports
       ├── client.py                # Supabase client configuration
       ├── conversation.py          # Conversation history functions
       ├── services.py              # Services management functions
       └── utils.py                 # Database utilities
├── tests/                           # Test suite
│   ├── __init__.py                  # Test package initialization
│   ├── test_client.py               # Client functionality tests
│   ├── test_conversation.py         # Conversation function tests
│   └── test_integration.py          # Integration tests
├── docs/                            # Documentation
├── examples/                        # Usage examples
├── scripts/                         # Utility scripts
├── config/                          # Configuration files
├── .env                            # Environment variables (not in repo)
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Dependencies
├── pyproject.toml                  # Modern Python project configuration
└── README.md                       # This file
```

## 🚀 Features

- **Easy Supabase Integration**: Simple setup and connection management
- **Conversation History**: Built-in functions for managing chat/conversation data
- **Services Management**: Complete API for managing services with flexible filtering
- **Environment Configuration**: Secure credential management with `.env` files
- **Type Hints**: Full type annotation support for better IDE experience
- **Comprehensive Testing**: Unit tests and integration tests included
- **Modern Python Packaging**: Uses `pyproject.toml` for configuration

## 📦 Installation

### Development Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd supabase_connector
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install in development mode:
```bash
pip install -e .
```

### Production Installation

```bash
pip install supabase-connector
```

## ⚙️ Configuration

1. Create a `.env` file in the project root:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
```

2. Make sure your Supabase database has the required tables (see Database Setup below).

## 🔧 Database Setup

Your Supabase database needs the following tables:

### Conversation History Table

```sql
CREATE TABLE conversation_history (
  id BIGSERIAL PRIMARY KEY,
  session_id TEXT NOT NULL,
  message JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes for better performance
CREATE INDEX idx_conversation_history_session_id ON conversation_history(session_id);
CREATE INDEX idx_conversation_history_created_at ON conversation_history(created_at);
```

### Services Table (Optional)

```sql
CREATE TABLE services (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  description TEXT,
  duration_minutes INTEGER,
  price DECIMAL(10,2),
  result_time TEXT,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes for better performance
CREATE INDEX idx_services_category ON services(category);
CREATE INDEX idx_services_is_active ON services(is_active);
CREATE INDEX idx_services_name ON services USING gin(to_tsvector('english', name));
```

### Info Table (Optional)

For company/contact information management (single record):

```sql
CREATE TABLE info (
  id BIGSERIAL PRIMARY KEY,
  name TEXT,
  phone TEXT,
  address TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  description TEXT,
  email TEXT
);

-- Insert your company info (single record)
INSERT INTO info (name, phone, address, email, description) VALUES
('Your Company Name', '+1234567890', '123 Main Street, City', 'contact@company.com', 'Company description');
```

## 📚 Usage

### Basic Usage

```python
from supabase_connector import SupabaseConnector, get_conversation_history, add_conversation_history

# Initialize connector (uses environment variables)
connector = SupabaseConnector()

# Test connection
if connector.test_connection():
    print("✅ Connected to Supabase!")
else:
    print("❌ Connection failed")

# Get conversation history
history = get_conversation_history()
print(f"Found {len(history)} conversations")

# Add new conversation
message = {
    "type": "human",
    "content": "Hello, how are you?",
    "timestamp": "2024-01-01T00:00:00Z"
}

result = add_conversation_history("session_123", message)
print("Message added successfully!")
```

### Services Management

```python
from supabase_connector import get_services, get_service_categories, get_services_summary

# Get all services
all_services = get_services()
print(f"Total services: {len(all_services)}")

# Get services by category
spa_services = get_services(category="spa")
print(f"Spa services: {len(spa_services)}")

# Search services by name (partial match)
massage_services = get_services(name="massage")
print(f"Services with 'massage': {len(massage_services)}")

# Get specific service by ID
service_list = get_services(service_id=1)
if service_list:
    service = service_list[0]
    print(f"Service: {service['name']} - ${service['price']}")

# Get only active services
active_services = get_services(is_active=True, limit=10)

# Combine multiple filters
filtered_services = get_services(
    category="spa", 
    name="massage", 
    is_active=True, 
    limit=5
)

# Get available categories
categories = get_service_categories()
print(f"Available categories: {categories}")

# Get services summary with statistics
summary = get_services_summary()
print(f"Total: {summary['total_services']}, Active: {summary['active_services']}")
```

### Info Management

Retrieve company/contact information from the single record in the `info` table:

```python
from supabase_connector import (
    get_info, get_info_name, get_info_phone, 
    get_info_address, get_info_email, get_info_description
)

# Get complete info record
info = get_info()
if info:
    print(f"Company: {info['name']}")
    print(f"Phone: {info['phone']}")
    print(f"Address: {info['address']}")

# Or get individual fields directly
company_name = get_info_name()
phone = get_info_phone()
address = get_info_address()
email = get_info_email()
description = get_info_description()

print(f"Contact {company_name} at {phone}")
print(f"Visit us at: {address}")

# Example usage in applications
def display_contact_info():
    name = get_info_name()
    phone = get_info_phone()
    email = get_info_email()
    
    contact_details = []
    if name:
        contact_details.append(f"Company: {name}")
    if phone:
        contact_details.append(f"Phone: {phone}")
    if email:
        contact_details.append(f"Email: {email}")
    
    return " | ".join(contact_details)
```

### Advanced Usage

```python
from supabase_connector import SupabaseConnector
from supabase_connector.conversation import get_conversation_by_session, delete_conversation_history
from supabase_connector.utils import check_table_exists, list_available_tables

# Custom connector with explicit credentials and schema
connector = SupabaseConnector()

# Check if tables exist
if check_table_exists("conversation_history"):
    print("Conversation table exists!")
    
    # Get conversations for specific session
    session_conversations = get_conversation_by_session("session_123")
    print(f"Found {len(session_conversations)} messages in session")
    
    # Delete all conversations for a session
    delete_conversation_history("old_session")
    print("Old conversations deleted")

if check_table_exists("services"):
    print("Services table exists!")
else:
    print("Available tables:")
    tables = list_available_tables()
    for table in tables:
        print(f"  - {table}")

# Direct client access for custom operations
client = connector.get_client()
response = client.table('services').select('name, category').limit(5).execute()
print(f"Custom query returned: {len(response.data)} records")
```

## 🚀 Quick Commands

### Test Services from Terminal

```bash
# Test all services functionality
python scripts/test_services.py

# Run comprehensive services example
python examples/services_usage.py

# Quick queries from command line
python -c "from src.supabase_connector import get_services; print(f'Total services: {len(get_services())}')"

python -c "from src.supabase_connector import get_service_categories; print(f'Categories: {get_service_categories()}')"

python -c "from src.supabase_connector import get_services; print(get_services(category='spa', limit=3))"

python -c "from src.supabase_connector import get_services; services = get_services(service_id=1); print(services[0] if services else 'Not found')"
```

### Test Info Management from Terminal

```bash
# Test info functionality
python examples/info_usage.py

# Quick info queries from command line
python -c "from src.supabase_connector import get_info; info = get_info(); print(info)"

python -c "from src.supabase_connector import get_info_name, get_info_phone; print(f'{get_info_name()}: {get_info_phone()}')"

python -c "from src.supabase_connector import get_info_address; print(f'Visit us at: {get_info_address()}')"

python -c "from src.supabase_connector import get_info_email; email = get_info_email(); print(f'Email: {email}' if email else 'No email configured')"
```

### Test Connection and Setup

```bash
# Test basic connection
python scripts/test_new_structure.py

# Run database setup helper
python examples/database_setup.py

# Test conversation functions
python examples/basic_usage.py
```

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/test_client.py tests/test_conversation.py

# Integration tests (requires real Supabase instance)
pytest tests/test_integration.py
```

### Test Connection

```bash
# Test your Supabase connection
python tests/test_integration.py
```

## � Complete API Reference

### Core Functions

#### SupabaseConnector
- `SupabaseConnector(schema="public")` - Initialize connector with optional schema
- `connector.test_connection()` - Test database connection
- `connector.get_client()` - Get configured Supabase client

#### Conversation Management
- `get_conversation_history()` - Get all conversation records
- `add_conversation_history(session_id, message)` - Add new conversation
- `get_conversation_by_session(session_id)` - Get conversations for specific session
- `delete_conversation_history(session_id)` - Delete session conversations

#### Services Management
- `get_services(service_id=None, name=None, category=None, is_active=None, limit=None)` - Main services function with flexible filtering
- `get_service_categories()` - Get list of unique service categories
- `get_services_summary()` - Get statistical summary of services

#### Info Management
- `get_info()` - Get complete info record as dictionary
- `get_info_name()` - Get company/contact name
- `get_info_phone()` - Get phone number
- `get_info_address()` - Get physical address
- `get_info_email()` - Get email address
- `get_info_description()` - Get description text
- `get_info_created_at()` - Get creation timestamp
- `get_info_id()` - Get record ID

#### Utilities
- `check_table_exists(table_name)` - Check if table exists
- `list_available_tables()` - List accessible tables

### Function Parameters

#### get_services() Parameters
- **service_id** (int, optional): Filter by specific service ID
- **name** (str, optional): Filter by service name (partial match, case-insensitive)
- **category** (str, optional): Filter by exact category match
- **is_active** (bool, optional): Filter by active status (True/False)
- **limit** (int, optional): Maximum number of records to return

#### Examples of get_services() Usage
```python
# Get all services
all_services = get_services()

# Get specific service
service = get_services(service_id=1)

# Get services by category
spa_services = get_services(category="massage therapy")

# Search by name (partial)
massage_services = get_services(name="deep tissue")

# Only active services
active = get_services(is_active=True)

# Combined filters
filtered = get_services(
    category="spa",
    name="massage", 
    is_active=True,
    limit=10
)
```

## 🔍 Troubleshooting

### Common Issues

1. **"Table doesn't exist" or "permission denied for schema"**
   - Create the required tables using SQL in Database Setup section
   - Check if you're using the correct schema (default: "public")
   - Verify your Supabase user has permissions to access the schema

2. **"Supabase credentials not found"**
   - Make sure your `.env` file is in the project root
   - Verify the environment variable names: `SUPABASE_URL` and `SUPABASE_ANON_KEY`

3. **"Connection failed"**
   - Check your internet connection
   - Verify your Supabase URL and key are correct
   - Make sure your Supabase project is active
   - Check if you need to use the service role key instead of anon key

### Debug Mode

Set environment variable for verbose logging:
```bash
export SUPABASE_DEBUG=1
```

## 🛠️ Development

### Project Setup for Contributors

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

3. Run tests before committing:
```bash
pytest
black src/ tests/
flake8 src/ tests/
mypy src/
```

### Adding New Features

1. Add your code in the appropriate module under `src/supabase_connector/`
2. Add tests in `tests/`
3. Update documentation
4. Run the test suite

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you have any questions or issues, please:

1. Check the troubleshooting section above
2. Look at existing issues in the repository
3. Create a new issue with detailed information about your problem

## � Schema Configuration

### Using Custom Schemas

If you need to work with a specific schema (e.g., "chatbot"):

```python
# Initialize connector with custom schema
connector = SupabaseConnector(schema="chatbot")

# Or modify client.py to set default schema
```

**Note**: Make sure your Supabase user has permissions for the custom schema.

## �🔄 Migration from Old Structure

If you're migrating from the old flat file structure:

1. Update your imports:
   ```python
   # For development (from project root)
   from src.supabase_connector import get_services, get_conversation_history
   
   # After installation
   from supabase_connector import get_services, get_conversation_history
   ```

2. Services API is new - replace any custom service queries with the new functions
3. Conversation API remains the same for backward compatibility

## 🎯 Project Roadmap

- [x] Core Supabase connection management
- [x] Conversation history functionality  
- [x] Services management with flexible filtering
- [x] Comprehensive testing suite
- [x] Modern Python packaging
- [ ] Real-time subscriptions support
- [ ] Batch operations for large datasets  
- [ ] Advanced query builders
- [ ] Plugin system for custom extensions