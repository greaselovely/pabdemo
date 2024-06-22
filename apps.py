import os
import json
import random
import requests
from util import clear, initialize_config, print_notice, format_timestamp

def retrieve_applications(api_key, api_url, apps_file="applications.json"):
    """
    Retrieve application data from the API or local file.

    This function attempts to fetch application data from the specified API endpoint
    using the provided API key. If successful and a local file doesn't exist, it saves
    the data to a JSON file. If the local file already exists, it reads the data from
    the file instead of making an API call.

    Args:
    api_key (str): The API key for authentication.
    api_url (str): The URL of the API endpoint for retrieving applications.
    apps_file (str, optional): The name of the local JSON file to store/read application data.
                               Defaults to "applications.json".

    Returns:
    dict: A dictionary containing the application data.

    Raises:
    requests.RequestException: If there's an error in making the API request.
    json.JSONDecodeError: If there's an error in parsing the API response or local file.
    IOError: If there's an error in reading from or writing to the local file.
    """
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    if not os.path.exists(apps_file):
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            apps = response.json()
            with open(apps_file, "w") as f:
                json.dump(apps, f, indent=4)
        except (requests.RequestException, json.JSONDecodeError, IOError) as e:
            print_notice(f"Error retrieving or saving application data: {e}", '!')
            raise
    else:
        try:
            with open(apps_file, "r") as f:
                apps = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print_notice(f"Error reading application data from file: {e}", '!')
            raise
    
    return apps

def print_random_apps(apps, num_apps=3, url_limit=5):
    """
    Select and print information about a specified number of random applications.

    Args:
    apps (dict): A dictionary containing the 'applications' list.
    num_apps (int): Number of random applications to select and print. Default is 3.
    url_limit (int): Maximum number of URLs to display for each application. Default is 5.
    """
    try:
        selected_apps = random.sample(apps['applications'], num_apps)
    except KeyError:
        print_notice("Error: 'applications' key not found in the data.", '!')
        return
    except ValueError as e:
        print_notice(f"Error selecting random apps: {e}", '!')
        return

    for app in selected_apps:
        print_notice(f"Name: {app.get('name', 'N/A')}")
        print_notice(f"Category: {app.get('category', 'N/A')}")
        print_notice(f"Reputation: {app.get('reputation', 'N/A')}")
        print_notice("URLs:")
        
        urls = app.get('urls', [])
        for url in urls[:url_limit]:
            print(f"\t{url}")
        
        if len(urls) > url_limit:
            remaining = len(urls) - url_limit
            print(f"\t  and {remaining} more URL{'s' if remaining > 1 else ''}")
        
        print("\n")

def main():
    clear()
    config = initialize_config()
    api_key = config.get("api_key", "")
    api_url = config.get("api_url", "") + "v1/applications"
    apps_file = "applications.json"

    try:
        apps = retrieve_applications(api_key, api_url, apps_file)
        print_random_apps(apps)
    except Exception as e:
        print_notice(f"An error occurred: {e}", '!')

if __name__ == "__main__":
    main()