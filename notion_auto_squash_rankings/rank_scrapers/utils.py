"""Defines utils functions for RankScrapers.

Functions:
    get_bs4_from_url(url: str) -> BeautifulSoup: 
        Send an HTTP GET request to the url given and if it succeeds, 
        returns a BeautifulSoup instance with the corresponding HTML.
        If not, returns None.
"""

from requests import get
from bs4 import BeautifulSoup

def get_bs4_from_url(url: str) -> BeautifulSoup:
    """Send an HTTP GET request to the url given and if it succeeds, 
       returns a BeautifulSoup instance with the url HTML.
       If not, returns None.

    Args:
        url (str): The url to get the html from.

    Returns:
        BeautifulSoup: BeautifulSoup instance with the url HTML if successful, 
                       None otherwise.
    """
    
    response = get(url, allow_redirects=False)
    if not response.ok:
        return None
    return BeautifulSoup(response.text, "html5lib")