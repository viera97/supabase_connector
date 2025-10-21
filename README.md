# Supabase Connector

A Python package for connecting and interacting with Supabase databases. This package provides easy-to-use functions for managing conversation history and other database operations.

## 🏗️ Project Structure

```
supabase_connector/
├── src/
│   └── supabase_connector/          # Main package source code
│       ├── __init__.py              # Package initialization and exports
│       ├── client.py                # Supabase client configuration
│       ├── conversation.py          # Conversation history functions
│       └── utils.py                 # Database utilities
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

Your Supabase database needs a `conversation_history` table. Here's the SQL to create it:

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

### Advanced Usage

```python
from supabase_connector import SupabaseConnector
from supabase_connector.conversation import get_conversation_by_session, delete_conversation_history
from supabase_connector.utils import check_table_exists, list_available_tables

# Custom connector with explicit credentials
connector = SupabaseConnector(
    url="your_supabase_url",
    key="your_supabase_key"
)

# Check if table exists
if check_table_exists("conversation_history"):
    print("Table exists!")
    
    # Get conversations for specific session
    session_conversations = get_conversation_by_session("session_123")
    print(f"Found {len(session_conversations)} messages in session")
    
    # Delete all conversations for a session
    delete_conversation_history("old_session")
    print("Old conversations deleted")
else:
    print("Table doesn't exist. Available tables:")
    tables = list_available_tables()
    for table in tables:
        print(f"  - {table}")
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

## 🔍 Troubleshooting

### Common Issues

1. **"Table 'conversation_history' doesn't exist"**
   - Create the table using the SQL provided in Database Setup
   - Or check if you're using the correct schema

2. **"Supabase credentials not found"**
   - Make sure your `.env` file is in the project root
   - Verify the environment variable names: `SUPABASE_URL` and `SUPABASE_ANON_KEY`

3. **"Connection failed"**
   - Check your internet connection
   - Verify your Supabase URL and key are correct
   - Make sure your Supabase project is active

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

## 🔄 Migration from Old Structure

If you're migrating from the old flat file structure:

1. Update your imports:
   ```python
   # Old way (still works but deprecated)
   from supabase_connector import get_conversation_history
   
   # New way (recommended)
   from supabase_connector import get_conversation_history
   ```

2. The API remains the same, so your existing code should work without changes.