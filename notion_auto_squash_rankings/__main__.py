from rank_scrapers import WorldRankScraper, FrenchRankScraper
from notion_writers import WorldRankWriter, FrenchRankWriter
from argument_utils import (
    get_notion_api_key, 
    get_world_db_id,
    get_french_db_id,
    get_gender
)

def main():
    # Get needed script parameters
    api_key = get_notion_api_key()
    if api_key is None:
        print(
            "No API key found.\n" +
            "Please provide a valid API key as the first command argument."
        )
        return

    world_db_id = get_world_db_id()
    french_db_id = get_french_db_id()

    if world_db_id is None and french_db_id is None:
        print(
            "No database id found.\n" + 
            "Please provide a world or french database id as a command" +
            " line argument (world=[db_id] or french=[db_id])."
        )
        return

    gender = get_gender()

    # If world db id given, scrap and update world ranking
    if world_db_id is not None:
        try:
            updateWorked = WorldRankWriter(
                api_key,
                world_db_id
            ).update_db(WorldRankScraper.scrap(men=gender))
        except:
            updateWorked = False

    # If french db id given, scrap and update french ranking
    elif french_db_id is not None:
        updateWorked = FrenchRankWriter(
            api_key,
            french_db_id
        ).update_db(FrenchRankScraper.scrap(men=gender))

    # Print updates result
    db_name = "World" if world_db_id is not None else "French"
    if updateWorked:
        print(
            f"{db_name} ranking successfully updated. " + 
              "Go check your notion page :)"
        )
    else:
        print(
            f"{db_name} ranking failed to update.\n" + 
            "Please check the validity of the keys given, " + 
            "and the structure of your database " + 
            "columns are correctly defined:\n" + 
            "Title column: Player's name (text)\n" +
            "Rank column: Rank (number)\n" +
            "Date column: Date (date: day/month/year)\n" +
            "Country column (if world ranking wanted): Country (text)"
        )
        
if __name__ == "__main__":
    main()