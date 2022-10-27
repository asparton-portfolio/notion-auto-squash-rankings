from bs4 import BeautifulSoup

from rank_scrapers.utils import get_bs4_from_url

class WorldRankScraper:
    """RankScraper able to get the world rankings.

    Class methods:
        scrap(*, men=True, nb_players=10) -> list[dict]:
            Scraps the world ranking information of nb_players players.
    """
    
    _ROOT_SCRAP_URL = 'http://www.squashinfo.com/rankings/'
        
    @staticmethod
    def scrap(*, men=True, nb_players=10) -> list[dict]:
        """Scraps the world ranking information of nb_players players.

        Args:
            men (bool, optional): To scrap men ranking. Defaults to True.
            nb_players (int, optional): Number of players to scrap. Defaults to 10.

        Returns:
            list[dict]: The scrapped information (player's name, rank, country)
        """
        
        scrap_url = WorldRankScraper._ROOT_SCRAP_URL
        scrap_url += 'men' if men else 'women'
        
        scrap_res = []
        
        doc = get_bs4_from_url(scrap_url)
        
        players_info = WorldRankScraper._get_players_ranking_info(doc, nb_players)
        for player_info in players_info:
            scrap_res.append({
                'name': WorldRankScraper._get_player_name(player_info),
                'country': WorldRankScraper.__get_player_country(player_info),
                'rank': WorldRankScraper._get_player_rank(player_info),   
            })
            
        return scrap_res
        
    @staticmethod  
    def _get_players_ranking_info(bs4_root: BeautifulSoup, limit=10) -> list[BeautifulSoup]:
        """Retrieve and returns the players ranking information from the given 
           bs4 instance assumed as document root tag.

        Args:
            bs4_root (BeautifulSoup): The root tag of the document
            limit (int, optional): The number of players to get. Defaults to 10.

        Returns:
            list[BeautifulSoup]: The HTML table rows containing the information.
        """
        
        return bs4_root.find('tbody').find('tr').find_all_next('tr', limit=limit)
    
    @staticmethod
    def _get_player_name(table_row: BeautifulSoup) -> str:
        """Get the player's name from the given bs4 HTML table row.

        Args:
            table_row (BeautifulSoup): The bs4 HTML tr containing the player's 
                                       information.

        Returns:
            str: The player's name
        """
        
        return table_row.findChildren()[2].string
    
    @staticmethod
    def _get_player_rank(table_row: BeautifulSoup) -> int:
        """Get the player's actual rank from the given bs4 HTML table row.

        Args:
            table_row (BeautifulSoup): The bs4 HTML tr containing the player's 
                                       information.

        Returns:
            int: The player's rank
        """
        
        return int(table_row.findChildren()[0].string)
    
    @staticmethod
    def __get_player_country(table_row: BeautifulSoup) -> int:
        """Get the player's country from the given bs4 HTML table row.

        Args:
            table_row (BeautifulSoup): The bs4 HTML tr containing the player's 
                                       information.

        Returns:
            str: The player's country
        """
        
        return table_row.findChildren()[6].string