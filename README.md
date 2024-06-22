# Prisma Access Browser API Demo

This project contains demo scripts for interacting with the Prisma Access Browser API. It includes utilities for configuration management, user information retrieval, and application data handling.

## Files

- `util.py`: Utility functions for configuration management and data formatting.
- `users.py`: Script to retrieve and display user information.
- `apps.py`: Script to fetch application data and display random selections.

## Setup

1. Ensure you have Python 3.12 installed on your system.

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the scripts for the first time to generate a `config.json` file.

4. Edit the `config.json` file with your Prisma Access Browser API key, API URL, and your Prisma Access Browser account email address (evereast.co).

5. Set the 'updated' field to 'true' in the `config.json` file.

## Usage

### User Information

To retrieve and display user information:

```
python users.py
```

This script will display the following information for the user associated with the email address in your config:
- Name
- Email
- Authentication Provider
- First Seen timestamp
- Last Seen timestamp

### Application Data

To fetch application data and display random selections:

```
python apps.py
```

This script will:
1. Fetch application data from the Prisma Access Browser API.
2. Save the data to `applications.json` if it doesn't exist.
3. Display information for 3 random applications, including:
   - Name
   - Category
   - Reputation
   - Up to 5 URLs (with a count of additional URLs if applicable)

## Configuration

The `config.json` file contains the following fields:
- `version`: Configuration version (do not modify manually)
- `api_key`: Your Prisma Access Browser API key
- `api_url`: The base URL for the Prisma Access Browser API
- `email_address`: Your email address associated with the Prisma Access Browser account
- `updated`: Set to 'true' after updating the config file

## Notes

- Ensure your API key has the necessary permissions to access user and application data.
- The scripts use local timezone for displaying timestamps.
- If you encounter any issues, check your `config.json` file and ensure all fields are correctly populated.

