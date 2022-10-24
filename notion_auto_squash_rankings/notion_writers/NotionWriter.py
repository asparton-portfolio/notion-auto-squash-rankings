from abc import ABC, abstractmethod
from notion_writers.utils import query_notion

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
    """

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