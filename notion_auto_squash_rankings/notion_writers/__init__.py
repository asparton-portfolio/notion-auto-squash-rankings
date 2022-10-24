"""Package used to update the notion databases associated with the 
   squash players ranking.

Modules:
    NotionWriter: Base abstract class defining how to update the Notion database 
                  associated with the squash players ranking.
    WorldRankWriter: NotionWriter for updating a world players ranking database.
    FrenchRankWriter: NotionWriter for updating a french players ranking database.
"""

from notion_writers.WorldRankWriter import WorldRankWriter
from notion_writers.FrenchRankWriter import FrenchRankWriter