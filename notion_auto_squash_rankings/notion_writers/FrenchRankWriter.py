from notion_writers.NotionWriter import NotionWriter
from notion_writers.utils import query_notion
from json import dumps as json_dumps

class FrenchRankWriter(NotionWriter):
    """NotionWriter for updating a french players ranking database.

    Instance methods:
        __init__(self, notion_api_key: str, db_id: str):
            Set and verify the personal notion notion_api_key and db_id for 
            further use.
        update_db(self, player_ranking: list[dict]) -> bool:
            Update the database with the given players ranking information,
            updating current pages and creating new ones if necessary.
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
        
        NotionWriter.__init__(self, notion_api_key, db_id)
        
    def update_db(self, players_ranking: list[dict]) -> bool:
        """Update the database with the given players ranking information,
           updating current pages and creating new ones if necessary.

        Args:
            players_ranking (list[dict]): The players ranking information.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        
        pages_id = self.get_current_pages_id()
        
        for player_ranking in players_ranking:
            method = "POST"
            api_endpoint = "/pages"
            if len(pages_id) > 0:
                method = "PATCH"
                api_endpoint += f"/{pages_id[0]}"
                pages_id.remove(pages_id[0])
              
            response = query_notion(
                api_endpoint,
                method=method,
                notion_api_key=self.notion_api_key,
                data=json_dumps(
                    NotionWriter.build_page_object(
                        self, 
                        player_ranking, 
                        method == "POST"
                    )
                )
            )
            
            if not response.ok:
                return False
            
        # Remove the other pages of the db if needed
        if len(pages_id) > 0:
            return self.delete_pages(self, pages_id)
            
        return True