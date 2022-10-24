"""Defines utils functions for RankScrapers.

Functions:
    get_bs4_from_url(url: str) -> BeautifulSoup: 
        Send an HTTP GET request to the url given and if it succeeds, 
        returns a BeautifulSoup instance with the corresponding HTML.
        If not, returns None.
"""

from requests import get
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

from bs4 import BeautifulSoup

def get_bs4_from_url(url: str, dynamic_page=False) -> BeautifulSoup:
    """Send an HTTP GET request to the url given and if it succeeds, 
       returns a BeautifulSoup instance with the url HTML.
       If not, returns None.

    Args:
        url (str): The url to get the html from.
        dynamic_page (bool): If True, use selenium to wait for the page to 
                             load its JS. Defaults to False.

    Returns:
        BeautifulSoup: BeautifulSoup instance with the url HTML if successful, 
                       None otherwise.
    """
    
    if dynamic_page:
        return get_bs4_from_dynamic_url(url)
    
    response = get(url, allow_redirects=False)
    if not response.ok:
        return None
    return BeautifulSoup(response.text, "html5lib")

def get_bs4_from_dynamic_url(url: str) -> BeautifulSoup:
    """Retrieve the loaded HTML of the page at the given URL using Selenium.

    Args:
        url (str): The URL of the page to retrieve the HTML of.

    Returns:
        BeautifulSoup: BeautifulSoup instance with the url HTML.
    """
    
    # Setup firefox driver
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = Firefox(service=Service(GeckoDriverManager().install()),
                     options=firefox_options)
    
    # Fetch html of page
    driver.get(url)
    html = driver.find_element("xpath", "//body").get_attribute("innerHTML")
    driver.quit()
    
    return BeautifulSoup(html, "html5lib")