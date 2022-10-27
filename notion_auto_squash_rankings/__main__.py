from rank_scrapers import WorldRankScraper, FrenchRankScraper
from notion_writers import (
    NotionWriter,
    WorldRankWriter,
    FrenchRankWriter,
    NotionAPIException
)
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
            'No API key found.\n' +
            'Please provide a valid API key as the first command argument.'
        )
        return

    world_db_id = get_world_db_id()
    french_db_id = get_french_db_id()

    if world_db_id is None and french_db_id is None:
        print(
            'No database id found.\n' +
            'Please provide a world or french database id as a command' +
            ' line argument (world=[db_id] or french=[db_id]).'
        )
        return

    gender = get_gender()

    if world_db_id is not None:
        print_script_result(
            update_database(
                gender,
                api_key,
                world_db_id,
                WorldRankScraper,
                WorldRankWriter
            ),
            "World"
        )
    else:
        print_script_result(
            update_database(
                gender,
                api_key,
                french_db_id,
                FrenchRankScraper,
                FrenchRankWriter
            ),
            "French"
        )


def update_database(
    fetch_male: bool,
    api_key: str,
    db_id: str,
    rank_scraper: FrenchRankScraper | WorldRankScraper,
    notion_writer: NotionWriter
) -> bool:
    """Try to performs the updates on the Notion database.

    Args:
        fetch_male (bool): True to fetch the male ranking, False to fetch
                           woman ranking.
        api_key (str): The Notion API key needed to perform the API calls.
        db_id (str): The id of the Notion database to be updated.
        rank_scraper (FrenchRankScraper | WorldRankScraper):
            The rank scraper class associated with the database to update 
            (world, french).
        notion_writer (NotionWriter): The Notion writer class associated with 
                                      the database to update (world, french).

    Returns:
        bool: True if the database was successfully updated, False otherwise.
    """

    try:
        return notion_writer(
            api_key,
            db_id
        ).update_db(rank_scraper.scrap(men=fetch_male))
    except NotionAPIException:
        return False


def print_script_result(update_worked: bool, updated_db_name: str):
    """Prints in the console a success message if the database update went
       well, and an error with possible solutions otherwise.

    Args:
        update_worked (bool): True if the database update was successful, 
                              False otherwise.
    """
    
    if update_worked:
        print(
            f'{updated_db_name} ranking successfully updated. ' +
            'Go check your notion page :)'
        )
    else:
        print(
            f'{updated_db_name} ranking failed to update.\n' +
            'Please check the validity of the keys given, ' +
            'and the structure of your database ' +
            'columns are correctly defined:\n' +
            "Title column: Player's name (text)\n" +
            'Rank column: Rank (number)\n' +
            'Date column: Date (date: day/month/year)\n' +
            'Country column (if world ranking wanted): Country (text)'
        )


if __name__ == '__main__':
    main()
