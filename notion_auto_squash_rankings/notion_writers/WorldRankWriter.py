from notion_writers.NotionWriter import NotionWriter
from notion_writers.utils import query_notion
from json import dumps as json_dumps

class WorldRankWriter(NotionWriter):
    """NotionWriter for updating a french world ranking database.

    Instance methods:
        __init__(self, notion_api_key: str, db_id: str):
            Set and verify the personal notion notion_api_key and db_id for 
            further use.
        update_db(self, player_ranking: list[dict]) -> bool:
            Update the database with the given players ranking information,
            updating current pages and creating new ones if necessary.
    """
    
    def __init__(self, notion_api_key: str, db_id: str):
        NotionWriter.__init__(self, notion_api_key, db_id)
        
    def update_db(self, players_ranking: list[dict]) -> bool:
        """Update the database with the given players ranking information,
           updating current pages and creating new ones if necessary.

        Args:
            players_ranking (list[dict]): The players ranking information.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        
        pages_id = self._get_current_pages_id()
        
        for player_ranking in players_ranking:
            method = 'POST'
            api_endpoint = '/pages'
            if len(pages_id) > 0:
                method = 'PATCH'
                api_endpoint += f'/{pages_id[0]}'
                pages_id.remove(pages_id[0])
              
            response = query_notion(
                api_endpoint,
                method=method,
                notion_api_key=self._notion_api_key,
                data=self._build_page_object(player_ranking, method == 'POST')
            )
            
            if not response.ok:
                return False
        
        # Remove the other pages of the db if needed
        if len(pages_id) > 0:
            return self._delete_pages(self, pages_id)
    
        return True
    
    def _build_page_object(self, page_info, to_post):
        """Build the page object to insert inside the database.

        Args:
            page_info dict: Contains the information about the player and its rank.
            to_post bool: If True, precise the parent database.

        Returns:
            dict: The dictionnary that will be used to insert or update a page.
        """
        
        page_object = NotionWriter._build_page_object(self, page_info, to_post)
        page_object['properties']['Country'] = {
            'rich_text': [
                {
                    'text': {
                        'content': NotionWriter._get_player_country(page_info['country'])
                    }
                }
            ]
        }
        
        return json_dumps(page_object)