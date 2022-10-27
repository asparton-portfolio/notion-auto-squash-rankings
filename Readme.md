# Notion auto squash rankings

Python script able to fill a Notion database with the squash french or world player's ranking.
![image](https://user-images.githubusercontent.com/65446617/198299627-86a3bac2-85a3-41a7-a0cc-3a5bfe849364.png)

## Prerequisites
### Notion
1. Create a [Notion](https://notion.so/) account
2. Create an integration and retrieve the **Internal Integration Token** ([see Notion documentation](https://developers.notion.com/docs/getting-started#step-1-create-an-integration))
3. Create a page containing a database with one of these columns:
<div>
  <img src="https://user-images.githubusercontent.com/65446617/198311122-5f233723-7a60-47d0-9649-639af87ed7ff.png" alt="world columns" width="45%" />
  <img src="https://user-images.githubusercontent.com/65446617/198311292-cf1bf78d-77c2-4770-ae56-510480888b37.png" alt="french columns" width="45%" />
</div>

3. Connect your integration to a page that will contain the database ([see Notion documentation](https://developers.notion.com/docs/getting-started#step-2-share-a-database-with-your-integration))
4. Retrieve the **database ID** ([see Notion documentation](https://developers.notion.com/docs/getting-started#step-2-share-a-database-with-your-integration))

### Python
1. Install [Python 3](https://www.python.org/downloads/)
2. Install [Poetry](https://python-poetry.org/docs/)

### Environment
1. Install [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new/)

## Installation
1. Clone this repository into your local machine
2. Open a terminal inside the directory and run:
```
poetry install
```

## How to use the script
```
poetry run python notion_auto_squash_rankings [API key] [Database type]=[Database ID] [gender]=["male"|"female"]
```

### Positional arguments
- 1: Internal Integration Token (API key) **Required**

### Named arguments
- french: The ID of a Notion database configured to receive french ranking.
- world: The ID of a Notion database configured to receive world ranking.
- gender("male"|"female") **Optional**: To fetch the male or female ranking. Male by default.

>❗Whether french or world argument must be given

### Examples
- Updating a database with the current female world ranking.
```
poetry run python notion_auto_squash_rankings secret_YuRSzSTdiaaSlw6s54uc1zNSUtCwVZcXe88L8BZBf9q world=c61dab96b1e2467b97796997717b81f0 gender=female
```

- Updating a database with the current male french ranking.
```
poetry run python notion_auto_squash_rankings secret_YuRSzSTdiaaSlw6s54uc1zNSUtCwVZcXe88L8BZBf9q french=0089eab25ebf4137a7e52075180da999
```
