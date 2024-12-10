import openai
import re
import json
import requests
import os

# Function to get the book data from below functions
def get_book_data(string):
    title, author = get_title_authour_chat_gpt(string)
    google_book_info = google_api_search(title, author)
    if(type(google_book_info) != dict):
        return google_book_info
    return google_json_to_db_json(google_book_info)

# Function to get the title and author of the book using ChatGPT
def get_title_authour_chat_gpt(book_string):
    content = book_string + "\n" + "What is this book? The book might have random charecters in that case do some smart changes. Finally give me these in json format: Title and Author"

    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),  
        organization=os.getenv("OPENAI_ORG_ID"),
        project=os.getenv("OPENAI_PROJECT_ID"),
    )

    stream = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL_ID"),
        messages=[{"role": "user", "content": content}],
        temperature=0.7,
        stream=True,
    )

    response = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response.append(chunk.choices[0].delta.content)

    json = extract_json_from_response(response)
    
    return json["Title"], json["Author"]

# Function to extract JSON from the response
def extract_json_from_response(response):
    response= "".join(response)

    # Extract JSON block using regex
    json_block = re.search(r"\n```json\n(.*?)\n```", response, re.DOTALL)

    # Convert the string to a Python dictionary
    title_author_json = json.loads(json_block.group(1))

    # Print the converted JSON
    return title_author_json

# Function to search for a book using the Google Books API
def google_api_search(title, author):
    # Google Books API URL
    url = os.getenv("GOOGLE_BOOKS_API_URL")
    
    # Query parameters
    params = {
        "q": f"intitle:{title}+inauthor:{author}",
    }
    
    # Send the GET request
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        if "items" in data:
            # Get the first book's details
            return data["items"][0]["volumeInfo"]
        else:
            return "No book found."
    else:
        return f"Error: {response.status_code} - {response.text}"

def google_json_to_db_json(book_info):
    transformed = {
        "title": book_info.get("title", ""),
        "subtitle": "",
        "author": ", ".join(book_info.get("authors", [])),
        "foreword": "",
        "editor": "",
        "illustrator": "",
        "creators": [],
        "synopsis": book_info.get("description", ""),
        "publisher": [book_info.get("publisher", "")],
        "characterEthnicity": [],
        "characterGenderIdentity": [],
        "characterRaceCulture": [],
        "characterReligion": [],
        "characterSexualOrientation": [],
        "awards": [],
        "contentWarning": [],
        "timePeriod": [],
        "narrativeForm": ["Non-fiction"] if book_info.get("printType", "").lower() == "book" else [],
        "genre": book_info.get("categories", []),
        "historicalEvents": [],
        "internationalAwards": [],
        "language": [book_info.get("language", "")],
        "languageRegister": [],
        "literaryDevices": [],
        "modesOfWriting": [],
        "pointOfView": [],
        "subject": [],
        "textFeatures": [],
        "textStructure": [],
        "topic": [],
        "voice": [],
        "tags": [],
        "isFiction": False,
        "isNonFiction": True,
        "isBlended": False,
        "guidedReadingLevel": "",
        "lexileLevel": "0",
        "hasMultiplePov": False,
        "hasUnreliableNarrative": False,
        "isbn10": [id_info["identifier"] for id_info in book_info.get("industryIdentifiers", []) if id_info["type"] == "ISBN_10"],
        "isbn13": [id_info["identifier"] for id_info in book_info.get("industryIdentifiers", []) if id_info["type"] == "ISBN_13"],
        "series": "",
        "seriesBookNumber": None,
        "seriesType": "Stand Alone",
        "defaultEdition": 0,
        "editions": [
            {
                "isbn10": [id_info["identifier"] for id_info in book_info.get("industryIdentifiers", []) if id_info["type"] == "ISBN_10"][0] if any(id_info["type"] == "ISBN_10" for id_info in book_info.get("industryIdentifiers", [])) else "",
                "isbn13": [id_info["identifier"] for id_info in book_info.get("industryIdentifiers", []) if id_info["type"] == "ISBN_13"][0] if any(id_info["type"] == "ISBN_13" for id_info in book_info.get("industryIdentifiers", [])) else "",
                "title": book_info.get("title", ""),
                "author": ", ".join(book_info.get("authors", [])),
                "image": book_info.get("imageLinks", {}).get("thumbnail", ""),
                "images": list(book_info.get("imageLinks", {}).values()),
                "pageCount": str(book_info.get("pageCount", "")),
                "wordCount": "0",
                "pubDate": book_info.get("publishedDate", ""),
                "copyrightDate": None,
                "foreword": "",
                "synopsis": book_info.get("description", ""),
                "edition": "",
                "legacy_id": None,
                "format": "Print and Digital" if book_info.get("readingModes", {}).get("text", False) else "Print",
                "isUnpaged": False,
            }
        ],
        "legacy_id": None,
        "created": None,
        "updated": None,
        "pubDate": book_info.get("publishedDate", ""),
        "images": list(book_info.get("imageLinks", {}).values()),
    }
    return transformed


