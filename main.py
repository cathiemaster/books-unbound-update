import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

BOOKS_UNBOUND_URL = "https://www.booksunboundpodcast.com/books"


def get_data(url):
    try:
        resp = requests.get(url)
        html = BeautifulSoup(resp.content, 'html.parser')
        return html

    except requests.HTTPError as http_ex:
        print(f"error! http exception: {http_ex}")

    except Exception as ex:
        print(f"error! other exception: {ex}")

def process_book_list(book_list):
    title_index = 0
    filtered_strings = ["so no books", "ariel:", "raeleen:"]
    booklist_df = pd.DataFrame(columns=["title", "author"])

    for b in book_list:
        book_content = [book for book in b.contents if (book != "<br/>") and (isinstance(book, str))]

        split_book_content = [{
            "title": book.split(" by ")[0], 
            "author": book.split(" by ")[1] if len(book.split(" by ")) > 1 else ""} 
            for book in book_content if not any(substring in book.lower() for substring in filtered_strings)]

        split_book_df = pd.DataFrame(split_book_content)
        booklist_df = pd.concat([booklist_df, split_book_df], ignore_index=True)

    return booklist_df


def main():
    print("------------ starting script ------------")
    html_soup = get_data(BOOKS_UNBOUND_URL)
    book_list = html_soup.find_all("p", class_="")
    booklist_df = process_book_list(book_list)
    filtered_booklist_df = booklist_df.drop_duplicates(subset=["title", "author"])

    print("------------ finished script ------------")


if __name__ == "__main__":
    main()

