from abc import ABC, abstractmethod

class RankScraper(ABC):
    """Base abstract class used to define the default RankScraper's behaviours.
    
    Instance methods:
        __init__(self, url, men): Instanciate a RankScraper that will be able 
                                   to scrap at the given url the ranking of 
                                   men or femen players.
        scrap(self) -> list[dict]: Scraps the RankScraper's url to retrieve 
                                   the players information.
    """
    
    def __init__(self, url: str, men=True):
        """Instanciate a RankScraper that will be able to scrap at the given 
           url the ranking of men or women players.

        Args:
            url (str): The url that the RankScraper will scrap.
            men (bool, optional): To whether get the men or femen ranking. Defaults to True.
        """
        
        self.url = url
        self.men = men
        
    @abstractmethod
    def scrap(self) -> list[dict]:
        """Scraps the RankScraper's url to retrieve the players information.

        Returns:
            list[dict]: A list containing the information scrapped.
        """
        
        pass