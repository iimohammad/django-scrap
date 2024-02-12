import requests
from bs4 import BeautifulSoup
import re
import time
from .models import Book


class ScrapData:
    def __init__(self, search_field, max_page) -> None:
        self.searchField = search_field
        self.max_page = max_page
        self.results = []
        self.scraping_complete = False  # Flag to indicate if scraping is complete

    def set_results(self, new_data):
        self.results.append(new_data)

    def get_results(self):
        return self.results

    def scrap_books(self):
        for item in range(1, self.max_page + 1):
            url = f"https://www.goodreads.com/search?page={item}&qid=b8PRNz7Ew7&query={self.searchField}&tab=books&utf8=%E2%9C%93"
            print(url)
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors
                soup = BeautifulSoup(response.content, "html.parser")
                books = soup.find_all("tr", {"itemtype": "http://schema.org/Book"})
                for book in books:
                    title = book.find("a", {"class": "bookTitle"}).text.strip()
                    author = book.find("span", {"itemprop": "author"}).find("span", {"itemprop": "name"}).text.strip()
                    rating = book.find("span", {"class": "minirating"}).text.strip()
                    string = "3.60 avg rating — 210,844 ratings — published 1962 — 330 editions"
                    year_match = re.search(r"published (\d{4})", string)
                    rating_match = re.search(r"(\d+\.\d+)", rating)

                    if year_match:
                        year_published = year_match.group(1)

                    if rating_match:
                        average_rating = rating_match.group(1)

                    new_data = {
                        'title': title,
                        'author': author,
                        'average_rating': average_rating,
                        'year_published': year_published
                    }

                    self.set_results(new_data)

                    Book.objects.create(
                        title=title,
                        author=author,
                        average_rating=average_rating,
                        year_published=year_published
                    )

                    print("Title:", title)
                    print("Author:", author)
                    print("Average Rating:", average_rating)
                    print("Year of Publication:", year_published)

                    print()

                print(f"----------finish page {item}--------------")
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while fetching page {item}: {e}")

            time.sleep(1)

        # Set scraping complete flag to True when scraping is finished
        self.scraping_complete = True

    def is_scraping_complete(self):
        return self.scraping_complete
