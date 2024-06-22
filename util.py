import os
import json
import sys
from colorama import Fore, Style
from datetime import datetime
from pytz import utc
from tzlocal import get_localzone

CURRENT_VERSION = 1  # Increment this when the config structure changes
DEFAULT_API_KEY = 'YOUR_API_KEY_HERE'
DEFAULT_API_URL = 'https://openapi.talon-sec.com/'
DEFAULT_EMAIL = 'YOUR_EMAIL_ADDRESS_HERE'

config_file = 'config.json'
default_config = {
    'version': CURRENT_VERSION,
    'api_key': DEFAULT_API_KEY,
    'api_url': DEFAULT_API_URL,
    'email_address': DEFAULT_EMAIL,
    'updated': 'false'
}

def clear():
    """
    Clear the terminal screen.

    This function uses the appropriate system command to clear the terminal
    screen based on the operating system. It uses 'cls' for Windows (nt) and
    'clear' for other operating systems (Unix-like systems).
    """
    os.system("cls" if os.name == "nt" else "clear")

def print_notice(message, indicator='i'):
    """
    Print a colored notice message to the console.

    This function prints a message with a colored indicator at the beginning.
    The indicator is enclosed in square brackets and colored either yellow
    for warnings ('!') or green for information ('i').

    Args:
    message (str): The message to be printed.
    indicator (str, optional): The indicator character to use. Defaults to 'i'.
        Use '!' for warnings (yellow) and 'i' for information (green).

    Note:
    This function uses colorama's Fore and Style for coloring the output.
    """
    color = Fore.YELLOW if indicator == '!' else Fore.GREEN
    print(f"{color}[{indicator}]{Style.RESET_ALL} {message}")

def initialize_config():
    """
    Initialize or validate the configuration file.
    
    This function checks for the existence of a 'config.json' file. If the file
    doesn't exist, it creates one with default values. If the file exists but
    doesn't match the current structure, it updates the structure while preserving
    existing values and resets the 'updated' flag to 'false'.

    Returns:
    dict: The configuration if successfully loaded and validated.

    Raises:
    SystemExit: If the config file needs to be updated by the user.
    """
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
        print_notice(f"Created {config_file} with default values. Please update it to execute these demo scripts.", '!')
        sys.exit(1)
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Check if the config structure needs updating
        if 'version' not in config or config['version'] < CURRENT_VERSION:
            updated_config = default_config.copy()
            for key in config:
                if key in updated_config and key != 'version':
                    updated_config[key] = config[key]
            updated_config['version'] = CURRENT_VERSION  # Ensure the version is updated
            updated_config['updated'] = 'false'  # Reset the 'updated' flag
            config = updated_config
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            print_notice(f"Updated {config_file} structure to version {CURRENT_VERSION}. Please review and update if necessary.", '!')
            sys.exit(1)

        if config.get('updated', 'false').lower() != 'true':
            print_notice(f"{config_file} needs to be reviewed and updated. Please update the values and set 'updated' to 'true'.", '!')
            sys.exit(1)
        
        return config

    except json.JSONDecodeError:
        print_notice(f"Error: {config_file} is not a valid JSON file. Please fix or delete it and run the script again.", '!')
        sys.exit(1)
    except IOError as e:
        print_notice(f"Error accessing {config_file}: {e}", '!')
        sys.exit(1)

def format_timestamp(timestamp_str):
    """
    Convert a UTC timestamp string to local time and format it.

    Args:
    timestamp_str (str): A timestamp string in ISO 8601 format.

    Returns:
    str: A formatted string in local time, in the format 'MM/DD/YYYY H:MM AM/PM'.
    """
    try:
        utc_time = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
        utc_time = utc_time.replace(tzinfo=utc)

        local_tz = get_localzone()
        local_time = utc_time.astimezone(local_tz)

        return local_time.strftime("%m/%d/%Y %I:%M %p")
    except ValueError:
        return "Invalid timestamp format"

if __name__ == "__main__":
    print_notice("This is a utility module and is not meant to be run directly.")