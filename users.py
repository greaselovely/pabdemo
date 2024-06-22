
import sys
import requests
from util import clear, initialize_config, print_notice, format_timestamp

def fetch_user_details(api_url, headers, params):
    """
    Fetch user details from the API.

    Args:
    api_url (str): The API endpoint URL.
    headers (dict): The headers for the API request.
    params (tuple): The query parameters for the API request.

    Returns:
    dict: The first user's details from the API response.

    Raises:
    requests.RequestException: If there's an error in the API request.
    IndexError: If no users are found in the response.
    KeyError: If the expected data is not in the response.
    """
    response = requests.get(api_url, headers=headers, params=params)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    data = response.json()
    return data['users'][0]

def main():
    """
    Main function to retrieve and display user information.

    This function initializes the configuration, makes an API call to fetch
    user details, and prints the user information to the console.

    The following user details are displayed:
    - Name
    - Email
    - Authentication Provider
    - First Seen timestamp
    - Last Seen timestamp

    Raises:
    SystemExit: If there's an error in configuration or API request.
    
    """
    clear()
    try:
        config = initialize_config()
        api_key = config["api_key"]
        api_url = config["api_url"] + "v1/users"
        email_address = config["email_address"]

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        params = (
            ('includeDeleted', 'false'),
            ('user.email', email_address),
            ('sort', 'user.name'),
            ('order', 'asc'),
        )

        user_details = fetch_user_details(api_url, headers, params)

        print_notice(f"Name: {user_details['name']}")
        print_notice(f"Email: {user_details['email']}")
        print_notice(f"Auth: {user_details['provider'].upper()}")
        print_notice(f"First Seen: {format_timestamp(user_details['firstSeen'])}")
        print_notice(f"Last Seen: {format_timestamp(user_details['lastSeen'])}")

    except KeyError as e:
        print_notice(f"Error: Missing key in configuration or API response: {e}", '!')
        sys.exit(1)
    except requests.RequestException as e:
        print_notice(f"Error making API request: {e}", '!')
        sys.exit(1)
    except Exception as e:
        print_notice(f"An unexpected error occurred: {e}", '!')
        sys.exit(1)

if __name__ == "__main__":
    main()