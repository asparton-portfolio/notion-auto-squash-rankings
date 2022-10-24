"""Defines utils functions for NotionWriters.

Functions:
    query_notion(endpoint: str, method: str, notion_api_key: str) -> Response:
        Build and send an HTTP request to the Notion API with the specified
        parameters.
"""

from requests import request
from requests import Response

def query_notion(endpoint: str, *, method="GET", notion_api_key: str) -> Response:
    """Build and send an HTTP request to the Notion API with the specified
       parameters.

    Args:
        endpoint (str): The end of the API point to query.
        method (str): The HTTP method of the request.
        notion_api_key (str): The Notion API key required to request the 
                              Notion API.

    Returns:
        Response: The request response.
    """
    
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Notion-Version": "2022-06-28"
    }
    return request(
        url=f"https://api.notion.com/v1{endpoint}",
        method=method, 
        headers=headers,
    )