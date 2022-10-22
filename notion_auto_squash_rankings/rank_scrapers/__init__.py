"""Package used to store classes able to scrap the squash players ranking.

Modules:
    RankScraper: Base abstract class used to define the default RankScraper's 
                 behaviours.
    WorldRankScraper: RankScraper able to get the world rankings.
    FrenchRankScraper: RankScraper able to get french rankings.
"""

from rank_scrapers.RankScraper import RankScraper
from rank_scrapers.WorldRankScraper import WorldRankScraper
from rank_scrapers.FrenchRankScraper import FrenchRankScraper