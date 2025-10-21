# Examples

This directory contains practical examples showing how to use the Supabase Connector package.

## Available Examples

### 1. Basic Usage (`basic_usage.py`)

Demonstrates the fundamental operations:
- Initializing the connector
- Testing connections
- Retrieving conversation history
- Adding new conversations

**Run it:**
```bash
python examples/basic_usage.py
```

### 2. Advanced Usage (`advanced_usage.py`)

Shows more sophisticated features:
- Session management
- Custom connector configurations
- Database utilities
- Error handling patterns

**Run it:**
```bash
python examples/advanced_usage.py
```

### 3. Database Setup (`database_setup.py`)

Helps you set up your Supabase database:
- Provides SQL schema for required tables
- Checks current database configuration
- Interactive setup wizard
- Verification of table operations

**Run it:**
```bash
python examples/database_setup.py
```

## Prerequisites

Before running these examples:

1. **Environment Setup**: Create a `.env` file in the project root:
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your-anonymous-key
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Tables**: Run the database setup example first:
   ```bash
   python examples/database_setup.py
   ```

## Running Examples

### From Project Root

```bash
# Basic usage
python examples/basic_usage.py

# Advanced features
python examples/advanced_usage.py

# Database setup help
python examples/database_setup.py
```

### From Examples Directory

```bash
cd examples

# Run any example
python basic_usage.py
python advanced_usage.py
python database_setup.py
```

## What Each Example Teaches

### Basic Usage
- How to initialize the connector
- Testing your Supabase connection
- Basic CRUD operations with conversation history
- Simple error handling

### Advanced Usage
- Managing conversations by session
- Creating custom connector instances
- Using database utility functions
- Comprehensive error handling
- Cleaning up test data

### Database Setup
- Understanding required database schema
- Setting up tables in Supabase
- Verifying database permissions
- Troubleshooting connection issues

## Example Output

When you run an example successfully, you'll see output like:

```
🚀 Supabase Connector - Basic Usage Example
==================================================
1️⃣ Initializing Supabase Connector...
✅ Connector initialized successfully!

2️⃣ Testing connection...
✅ Connection successful!

3️⃣ Retrieving conversation history...
✅ Found 5 conversation records

4️⃣ Adding a test conversation...
✅ Added conversation successfully! Records returned: 1

🎉 Basic usage example completed!
```

## Troubleshooting Examples

If examples fail, check:

1. **Environment Variables**: Make sure `.env` file exists with correct values
2. **Database Tables**: Run `database_setup.py` to create required tables
3. **Network Connection**: Verify internet connectivity to Supabase
4. **Permissions**: Check that your Supabase key has required permissions

## Customizing Examples

Feel free to modify these examples for your needs:

- Change session IDs and message content
- Add your own error handling
- Integrate with your application logic
- Use as templates for your own code

## Next Steps

After running these examples:

1. Read the [API documentation](../docs/README.md)
2. Check out the [test files](../tests/) for more usage patterns
3. Start building your own application using the connector
4. Contribute your own examples back to the project!