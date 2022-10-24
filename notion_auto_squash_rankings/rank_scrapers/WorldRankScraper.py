from bs4 import BeautifulSoup

from rank_scrapers.RankScraper import RankScraper
from rank_scrapers.utils import get_bs4_from_url

class WorldRankScraper(RankScraper):
    ROOT_URL = "http://www.squashinfo.com/rankings/"
    
    def __init__(self, men=True):
        """Instanciate a WorldRankScraper that will be able to scrap 
           information about men or women world squash ranking.

        Args:
            men (bool, optional): To scrap men or women ranking. Defaults to True.
        """
        
        RankScraper.__init__(
            self,
            WorldRankScraper.ROOT_URL + ("men" if men else "women"),
            men
        )
        
    def scrap(self) -> list[dict]:
        scrap_res = []
        
        doc = get_bs4_from_url(self.url)
        
        players_info = WorldRankScraper.get_players_ranking_info(doc)
        for player_info in players_info:
            scrap_res.append({
                "Player's name": WorldRankScraper.get_player_name(player_info),
                "Nationality": WorldRankScraper.get_player_country(player_info),
                "Rank": WorldRankScraper.get_player_rank(player_info),   
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
        
        return bs4_root.find("tbody").find("tr").find_all_next("tr", limit=limit)
    
    @staticmethod
    def get_player_name(table_row: BeautifulSoup) -> str:
        """Get the player's name from the given bs4 HTML table row.

        Args:
            table_row (BeautifulSoup): The bs4 HTML tr containing the player's 
                                       information.

        Returns:
            str: The player's name
        """
        
        return table_row.findChildren()[2].string
    
    @staticmethod
    def get_player_rank(table_row: BeautifulSoup) -> int:
        """Get the player's actual rank from the given bs4 HTML table row.

        Args:
            table_row (BeautifulSoup): The bs4 HTML tr containing the player's 
                                       information.

        Returns:
            int: The player's rank
        """
        
        return int(table_row.findChildren()[0].string)
    
    @staticmethod
    def get_player_country(table_row: BeautifulSoup) -> int:
        """Get the player's country from the given bs4 HTML table row.

        Args:
            table_row (BeautifulSoup): The bs4 HTML tr containing the player's 
                                       information.

        Returns:
            str: The player's country
        """
        
        return table_row.findChildren()[6].string