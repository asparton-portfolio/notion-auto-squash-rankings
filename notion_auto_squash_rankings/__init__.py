"""Script that scraps information about the squash world & french rankings,
   and update notion databases to visualize the players ranking.
   
Internal packages:
    rank_scrapers: Package used to store classes able to scrap the squash 
                   players ranking.
   
External packages:
    requests: HTTP requests needed to get the html of the pages to scrap and 
              use the Notion API.
    beautifulsoup4: The scraping library used to get the information about the 
                player's and their ranking.
"""