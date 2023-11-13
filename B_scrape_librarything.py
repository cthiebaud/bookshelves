import sys
import requests
from bs4 import BeautifulSoup

def add_book_to_library(isbn, username, password):
    session = requests.Session()

    # Step 1: Log in to your LibraryThing account.
    login_url = 'https://www.librarything.com/login_process.php'
    login_payload = {
        'membername': username,
        'password': password
    }

    # Login to your LibraryThing account.
    login_response = session.post(login_url, data=login_payload)

    # Check if the login was successful (you should add error handling here).
    if 'Welcome, ' + username in login_response.text:
        print("Successfully logged in to LibraryThing.")
    else:
        print("Login failed. Check your credentials.")
        return

    # Step 2: Search for the book by ISBN.
    search_url = f'https://www.librarything.com/isbn/{isbn}'
    search_response = session.get(search_url)

    # Step 3: Parse the search results and add the book to your library.
    soup = BeautifulSoup(search_response.text, 'html.parser')

    # Check if the book is found based on the ISBN.
    if 'No titles match your search' in soup.text:
        print(f"No book found for ISBN {isbn}.")
    else:
        add_button = soup.select_one('.add-to-your-books')

        if add_button:
            add_url = f'https://www.librarything.com/addbook/{add_button["data-book"]}'
            add_response = session.get(add_url)

            # Check if the book was successfully added.
            if 'Your book has been added to your books' in add_response.text:
                print(f"Book with ISBN {isbn} added to your LibraryThing library.")
            else:
                print(f"Failed to add the book with ISBN {isbn}.")
        else:
            print(f"No 'Add to your books' button found for ISBN {isbn}.")

if len(sys.argv) != 4:
    print("Usage: python add_book_to_library.py <ISBN> <Username> <Password>")
else:
    isbn = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    add_book_to_library(isbn, username, password)
