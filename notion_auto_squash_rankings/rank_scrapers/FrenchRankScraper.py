from bs4 import BeautifulSoup
from rank_scrapers.utils import get_selenium_from_url
from selenium.webdriver.common.by import By

class FrenchRankScraper:
    SCRAP_URL = "https://squashnet.fr/classements"
        
    def scrap(*, men=True, nb_players=10) -> list[dict]:
        if nb_players > 10:
            raise Exception("Can't scrap more than the first 10 players " + 
                            "for the french ranking.")
        
        scrap_res = []
        
        driver = get_selenium_from_url(FrenchRankScraper.SCRAP_URL)
        body = driver.find_element(By.XPATH, "//body").get_attribute("innerHTML")
        if not men:
            woman_label = driver.find_element(
                By.CSS_SELECTOR,
                "#filters .checkbox:nth-child(3) label"
            )
            woman_label.click()
            body = driver.find_element(By.XPATH, "//body").get_attribute("innerHTML")
        driver.close()

        players_info = FrenchRankScraper.get_players_ranking_info(BeautifulSoup(body, "html5lib"))
        for player_info in players_info:
            scrap_res.append({
                "name": FrenchRankScraper.get_player_name(player_info),
                "rank": FrenchRankScraper.get_player_rank(player_info),
            })
            
        return scrap_res
        
    @staticmethod  
    def get_players_ranking_info(bs4_root: BeautifulSoup, limit=10) -> list[BeautifulSoup]:
        """Retrieve and returns the players ranking information from the given 
           bs4 instance assumed as document root tag.

        Args:
            bs4_root (BeautifulSoup): The root tag of the document
            limit (int, optional): The number of players to get. Defaults to 10.

        Returns:
            list[BeautifulSoup]: The HTML table rows containing the information.
        """
        
        return bs4_root.find(
            "div", {"class": "row header"}
        ).find_all_next("div", class_="row", limit=limit)
    
    @staticmethod
    def get_player_name(table_row: BeautifulSoup) -> str:
        """Get the player's name from the given bs4 HTML table row.

        Args:
            table_row (BeautifulSoup): The bs4 HTML tr containing the player's 
                                       information.

        Returns:
            str: The player's name
        """
        
        full_name = table_row.findChildren()[3].string
        last_name = full_name.split()[0].capitalize()
        first_name = full_name.split()[1].capitalize()
        return f"{first_name} {last_name}"
    
    @staticmethod
    def get_player_rank(table_row: BeautifulSoup) -> int:
        """Get the player's actual rank from the given bs4 HTML table row.

        Args:
            table_row (BeautifulSoup): The bs4 HTML tr containing the player's 
                                       information.

        Returns:
            int: The player's rank
        """
        
        return int(table_row.findChildren()[5].string)