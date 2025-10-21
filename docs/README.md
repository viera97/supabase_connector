# Supabase Connector Documentation

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [API Reference](#api-reference)
4. [Configuration](#configuration)
5. [Examples](#examples)
6. [Troubleshooting](#troubleshooting)

## Installation

### Requirements

- Python 3.8 or higher
- Active Supabase project
- Supabase URL and anonymous key

### Install Package

```bash
pip install supabase-connector
```

### Development Installation

```bash
git clone <repository-url>
cd supabase_connector
pip install -e .
```

## Quick Start

### 1. Set Up Environment

Create a `.env` file:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anonymous-key
```

### 2. Basic Usage

```python
from supabase_connector import SupabaseConnector, get_conversation_history

# Initialize and test connection
connector = SupabaseConnector()
if connector.test_connection():
    print("Connected!")
    
    # Get conversation history
    conversations = get_conversation_history()
    print(f"Found {len(conversations)} conversations")
```

## API Reference

### SupabaseConnector Class

#### `__init__(url=None, key=None)`

Initialize the Supabase connector.

**Parameters:**
- `url` (str, optional): Supabase URL. Uses `SUPABASE_URL` env var if not provided.
- `key` (str, optional): Supabase key. Uses `SUPABASE_ANON_KEY` env var if not provided.

**Raises:**
- `ValueError`: If credentials are not provided and not found in environment.

#### `test_connection()`

Test the connection to Supabase.

**Returns:**
- `bool`: True if connection successful, False otherwise.

#### `get_client()`

Get the underlying Supabase client.

**Returns:**
- `Client`: The Supabase client instance.

### Conversation Functions

#### `get_conversation_history()`

Retrieve all conversation history records.

**Returns:**
- `List[Dict[str, Any]]`: List of conversation records.

**Raises:**
- `RuntimeError`: If the query fails.

#### `add_conversation_history(session_id, message)`

Add a new conversation record.

**Parameters:**
- `session_id` (str): Session identifier.
- `message` (Dict[str, Any]): Message data.

**Returns:**
- `List[Dict[str, Any]]`: Inserted record data.

**Raises:**
- `ValueError`: If session_id is empty or message is invalid.
- `RuntimeError`: If the insert fails.

#### `get_conversation_by_session(session_id)`

Get conversations for a specific session.

**Parameters:**
- `session_id` (str): Session identifier.

**Returns:**
- `List[Dict[str, Any]]`: Session conversation records.

#### `delete_conversation_history(session_id)`

Delete all conversations for a session.

**Parameters:**
- `session_id` (str): Session identifier.

**Returns:**
- `bool`: True if successful.

### Utility Functions

#### `check_table_exists(table_name, schema='public')`

Check if a table exists.

**Parameters:**
- `table_name` (str): Name of the table.
- `schema` (str): Schema name (default: 'public').

**Returns:**
- `bool`: True if table exists.

#### `list_available_tables()`

Get list of available tables.

**Returns:**
- `List[str]`: List of accessible table names.

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Your Supabase project URL | Yes |
| `SUPABASE_ANON_KEY` | Your Supabase anonymous key | Yes |
| `SUPABASE_DEBUG` | Enable debug logging | No |

### Database Schema

Required table structure for conversation history:

```sql
CREATE TABLE conversation_history (
  id BIGSERIAL PRIMARY KEY,
  session_id TEXT NOT NULL,
  message JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_conversation_history_session_id ON conversation_history(session_id);
```

## Examples

See the [examples](../examples/) directory for complete usage examples.

## Troubleshooting

### Common Errors

**"Table doesn't exist"**
- Create the required table in your Supabase database
- Check table permissions

**"Connection failed"**
- Verify your Supabase URL and key
- Check internet connectivity
- Ensure Supabase project is active

**"Import errors"**
- Make sure the package is installed: `pip install -e .`
- Check Python path configuration

### Debug Mode

Enable detailed logging:

```python
import os
os.environ['SUPABASE_DEBUG'] = '1'
```

### Getting Help

1. Check this documentation
2. Review the examples
3. Check existing issues in the repository
4. Create a new issue with detailed error information