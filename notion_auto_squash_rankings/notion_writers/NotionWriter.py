from abc import ABC, abstractmethod
from notion_writers.utils import query_notion
from datetime import datetime
from json import dumps as json_dumps

class NotionWriter(ABC):
    """Base abstract class defining how to update the Notion database 
       associated with the squash players ranking.

    Instance methods:
        __init__(self, notion_api_key: str, db_id: str):
            Set and verify the personal notion notion_api_key and db_id for 
            further use.
        update_db(self, player_ranking: list[dict]) -> bool:
            Abstract method that will be used to update the current database 
            with the given players ranking information.
        get_current_pages_id(self) -> list[str]:
            Retrieve the id of the pages currently present in the database.
        build_page_object(self, page_info: dict, to_post: bool) -> dict:
            Build the page object to insert inside the database.
    
    Class methods:
        get_player_emoji(player_rank: int) -> str:
            Returns an emoji describing the player depending on the given rank.
        get_player_country(player_country: str) -> str:
            Determine a pleasant way to present the given country.
    """

    # Supported countries
    countries = {
        "EGY": "🇪🇬 Egypt",
        "NZL": "🇳🇿 New Zealand",
        "ENG": "🇬🇧 England",
        "PER": "🇵🇪 Peru",
        "FRA": "🇫🇷 France",
        "WAL": "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Wales",
        "COL": "🇨🇴 Colombia",
        "IND": "🇮🇳 India",
        "SUI": "🇨🇭 Switzerland",
        "GER": "🇩🇪 Germany",
        "USA": "🇺🇸 United States",
        "QAT": "🇶🇦 Qatar",
        "SCO": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland",
        "MEX": "🇲🇽 Mexico",
        "ESP": "🇪🇸 Spain",
        "HKG": "🇭🇰 Hong-Kong",
        "PAK": "🇵🇰 Pakistan",
        "HUN": "🇭🇺 Hungary",
        "POR": "🇵🇹 Portugal",
        "ARG": "🇦🇷 Argentina",
        "CAN": "🇨🇦 Canada",
        "MAS": "🇲🇾 Malaysia",
        "JPN": "🇯🇵 Japan",
        "GUA": "🇬🇹 Guatemala",
        "BEL": "🇧🇪 Belgium",
        "RSA": "🇿🇦 South Africa"
    }

    def __init__(self, notion_api_key: str, db_id: str):
        """Set and verify the personal notion notion_api_key and db_id for 
           further use.

        Args:
            notion_api_key (str): The notion integration token to be able to 
                                  use the NotionAPI.
            db_id (str): The id the database associated in which to do the CRUD
                         operations with the further information.
        """
        
        # Check if the given notion api key and database id are valid
        res = query_notion(f"/databases/{db_id}", notion_api_key=notion_api_key)
        if not res.ok:
            raise Exception(res.json()["message"])
        
        self.notion_api_key = notion_api_key
        self.db_id = db_id
        
    @abstractmethod
    def update_db(self, players_ranking: list[dict]) -> bool:
        """Abstract method that will be used to update the current database 
           with the given players ranking information.

        Args:
            players_ranking (list[dict]): The players ranking information.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        
        pass
    
    def get_current_pages_id(self) -> list[str]:
        """Retrieve the id of the pages currently present in the database.

        Returns:
            list[str]: The list of the pages id or an empty list of no page.
        """
        
        pages_id = []
        
        for page in query_notion(
            f"/databases/{self.db_id}/query",
            method="POST",
            notion_api_key=self.notion_api_key
        ).json()["results"]:
            pages_id.append(page["id"])
            
        return pages_id
    
    def delete_pages(self, pages_id: list[str]) -> bool:
        """Try to delete the pages with the given id.

        Args:
            pages_id (list[str]): A list of the pages id to delete.

        Returns:
            bool: True if all pages were deleted successfully, False otherwise.
        """
        
        for page_id in pages_id:
            response = query_notion(
                f"/pages/{page_id}",
                method="PATCH",
                notion_api_key=self.notion_api_key,
                data=json_dumps({ "archived": True })
            )
            
            if not response.ok:
                return False
        
        return True
    
    def build_page_object(self, page_info: dict, to_post: bool) -> dict:
        """Build the page object to insert inside the database.

        Args:
            page_info dict: Contains the information about the player and its rank.
            to_post bool: If True, precise the parent database.

        Returns:
            dict: The dictionnary that will be used to insert or update a page.
        """
        
        page_object = {
            "icon": {
                "emoji": NotionWriter.get_player_emoji(page_info["rank"])
            },
            "properties": {
                "Player's name": {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": page_info["name"]
                            }
                        }
                    ]
                },
                "Rank": {
                    "number": page_info["rank"]
                },
                "Date": {
                    "date": {
                        "start": str(datetime.now().date()),
                        "end": None,
                        "time_zone": None
                    }
                }
            }
        }
        if (to_post):
            page_object["parent"] = { "database_id": self.db_id }
            
        return page_object
    
    @staticmethod
    def get_player_emoji(player_rank: int) -> str:
        """Returns an emoji describing the player depending on the given rank.

        Args:
            player_rank (int): The rank of the player to determine the emoji.

        Returns:
            str: The emoji associated with the given rank.
        """
        
        if player_rank == 1:
            return "🏅"
        elif player_rank == 2:
            return "🥈"
        elif player_rank == 3:
            return "🥉"
        else:
            return "👤"
        
    @staticmethod
    def get_player_country(player_country: str) -> str:
        """Determine a pleasant way to present the given country.

        Args:
            player_country (str): The country alpha-3 code.

        Returns:
            str: a pleasant way to present the given country if supported.
        """
        
        if player_country in NotionWriter.countries:
            return NotionWriter.countries[player_country]
        else:
            return player_country