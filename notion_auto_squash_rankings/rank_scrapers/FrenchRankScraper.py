from bs4 import BeautifulSoup

from rank_scrapers.RankScraper import RankScraper
from rank_scrapers.utils import get_bs4_from_url

class FrenchRankScraper(RankScraper):
    def __init__(self, men=True):
        """Instanciate a FrenchRankScraper that will be able to scrap 
           information about men or women french squash ranking.

        Args:
            men (bool, optional): To scrap men or women ranking. Defaults to True.
        """
        
        RankScraper.__init__(
            self,
            "https://squashnet.fr/classements",
            men
        )
        
    def scrap(self) -> list[dict]:
        scrap_res = []
        
        doc = get_bs4_from_url(self.url, True)

        players_info = FrenchRankScraper.get_players_ranking_info(doc)
        for player_info in players_info:
            scrap_res.append({
                "Player's name": FrenchRankScraper.get_player_name(player_info),
                "Rank": FrenchRankScraper.get_player_rank(player_info),
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
        
        return int(table_row.findChildren()[0].string)