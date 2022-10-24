from notion_writers.NotionWriter import NotionWriter

class FrenchRankWriter(NotionWriter):
    
    def __init__(self, notion_api_key: str, db_id: str):
        NotionWriter.__init__(self, notion_api_key, db_id)
        
    def update_db(self, players_ranking: list[dict]) -> bool:
        return False