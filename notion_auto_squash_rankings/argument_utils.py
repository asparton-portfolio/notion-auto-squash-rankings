"""Defines util functions used to retrieve the needed parameters to run the 
   script.

Functions:
    get_notion_api_key() -> str:
        Try to get the notion api key needed to call the Notion API.
    get_french_db_id() -> str:
        Try to get the french database id in which to write the information.
    get_world_db_id() -> str:
        Try to get the world database id in which to write the information.
    def get_gender() -> bool:
        Try to get the gender type to fetch wheter the men or women ranking.
    get_pair_argument(arg_position: int) -> tuple[str, str]:
        Try to retrieve the command line argument at the given position 
        assuming its a key value pair (key=value).
"""

from dotenv import dotenv_values
from sys import argv

def get_notion_api_key() -> str | None:
    """Try to get the notion api key needed to call the Notion API. 

    Returns:
        str: The Notion API key if given, None otherwise.
    """
    
    # First check if given a command line argument
    if (len(argv) > 1):
        return argv[1]
    return None

def get_french_db_id() -> str | None:
    """Try to get the french database id in which to write the information.

    Returns:
        str: The french database id if given, None otherwise.
    """
    
    arg_key, arg_val = get_pair_argument(2)
    if arg_key == 'french':
        return arg_val
    else:
        arg_key, arg_val = get_pair_argument(3)
        if arg_key == 'french':
            return arg_val
        return None

def get_world_db_id() -> str | None:
    """Try to get the world database id in which to write the information.

    Returns:
        str: The world database id if given, None otherwise.
    """
    
    arg_key, arg_val = get_pair_argument(2)
    if arg_key == 'world':
        return arg_val
    else:
        arg_key, arg_val = get_pair_argument(3)
        if arg_key == 'world':
            return arg_val
        return None
    
def get_gender() -> bool:
    """Try to get the gender type to fetch wheter the men or women ranking.

    Returns:
        bool: True if male, False otherwise.
    """
    
    arg_key, arg_val = get_pair_argument(2)
    if arg_key == 'gender':
        return arg_val == 'male'
    else:
        arg_key, arg_val = get_pair_argument(3)
        if arg_key == 'gender':
            return arg_val == 'male'
        return True

def get_pair_argument(arg_position: int) -> tuple[str, str] | tuple[None, None]:
    """Try to retrieve the command line argument at the given position 
       assuming its a key value pair (key=value).

    Args:
        arg_position (int): The position of the command line argument.

    Returns:
        tuple[str, str]: key: pair if found, (None, None) otherwise.
    """
    
    if (len(argv) < arg_position + 1):
        return None, None
    
    arg = argv[arg_position].split('=')
    if (len(arg) <= 1):
        return None, None
    
    return arg[0], arg[1]