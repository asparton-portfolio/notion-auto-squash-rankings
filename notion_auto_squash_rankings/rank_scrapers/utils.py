"""Defines internal utils functions for RankScrapers.

Functions:
    get_bs4_from_url(url: str) -> BeautifulSoup: 
        Send an HTTP GET request to the url given and if it succeeds, 
        returns a BeautifulSoup instance with the corresponding HTML.
        If not, returns None.
    get_selenium_from_url(url: str) -> Firefox:
        Create a selenium driver instance with the loaded url.
"""

from requests import get
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

from bs4 import BeautifulSoup

def get_bs4_from_url(url: str) -> BeautifulSoup | None:
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
    return BeautifulSoup(response.text, 'html5lib')

def get_selenium_from_url(url: str) -> Firefox:
    """Create a selenium driver instance with the loaded url.

    Args:
        url (str): The URL of the page to load the driver with.

    Returns:
        Firefox: BeautifulSoup instance with the url HTML.
    """
    
    # Setup firefox driver
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    driver = Firefox(
        service=Service(GeckoDriverManager().install()),
        options=firefox_options
    )
    
    # Go to page
    driver.get(url)
    return driver