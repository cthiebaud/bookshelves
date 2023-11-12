import json
import requests

openlibrary = {}

# Function to get book cover dimensions
def get_book_cover_size(isbn):
    # Define the Open Library API endpoint for book details
    api_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"

    try:
        # Make a GET request to the API
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP errors

        if response.status_code == 200:
            # Parse the JSON response
            book_data = response.json()
 
            openlibrary[isbn] = book_data

            with open('dist/openlibrary.json', 'w') as fp:
                json.dump(openlibrary, fp, indent=2)

            if f"ISBN:{isbn}" in book_data:
                book_info = book_data[f"ISBN:{isbn}"]
                
                # Check if cover is available
                if "cover" in book_info:
                    cover_info = book_info["cover"]
                    if "large" in cover_info:
                        cover_size = cover_info["large"]
                        return cover_size
                    else:
                        return "Cover size not available"
                else:
                    return "Cover not available"
            else:
                return "Book not found in Open Library"
        else:
            return "Failed to retrieve book data"
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")    
    except Exception as e:
        return f"Error: {str(e)}"

# ISBNs of the book you want to query
isbns = [line.strip() for line in open("isbn-ja.txt", 'r') if line.strip()]

for i, isbn in enumerate(isbns):

    # Get the cover size for the book
    cover_size = get_book_cover_size(isbn)
    print(f"Cover size for ISBN {isbn}: {cover_size}")

with open('dist/openlibrary.json', 'w') as fp:
    json.dump(openlibrary, fp, indent=2)

