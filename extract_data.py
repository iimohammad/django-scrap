from bs4 import BeautifulSoup
import requests
import csv

# List of URLs to process
urls = [
    "https://www.goodreads.com/list/show/26495.Best_Woman_Authored_Books?page=1",
    "https://www.goodreads.com/list/show/26495.Best_Woman_Authored_Books?page=2",
    "https://www.goodreads.com/list/show/26495.Best_Woman_Authored_Books?page=3",
    "https://www.goodreads.com/list/show/26495.Best_Woman_Authored_Books?page=4",
    "https://www.goodreads.com/list/show/26495.Best_Woman_Authored_Books?page=5",
]

# List to store book information
book_info_list = []

for url in urls:
    # Download HTML code from the provided URL
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text

        # Create BeautifulSoup object
        soup = BeautifulSoup(html, "html.parser")

        # Extracting information for multiple books
        books = soup.find_all("tr", itemscope=True, itemtype="http://schema.org/Book")

        for book in books:
            book_info = {}

            # Extracting book title
            title_tag = book.find("span", itemprop="name")
            book_info["title"] = title_tag.text.strip() if title_tag else None

            # Extracting author information
            author_tag = book.find("span", itemprop="author")
            book_info["author"] = (
                author_tag.find("span", itemprop="name").text.strip()
                if author_tag
                else None
            )

            # Extracting book rating and number of ratings
            rating_tag = book.find("span", class_="minirating")
            if rating_tag:
                rating_text = rating_tag.text.strip().split()
                book_info["average_rating"] = rating_text[0]
                book_info["ratings_count"] = rating_text[3].replace(",", "")

            # Extracting book cover image URL
            cover_img_tag = book.find("img", itemprop="image")
            book_info["cover_image_url"] = (
                cover_img_tag["src"] if cover_img_tag else None
            )

            # Append book information to the list
            book_info_list.append(book_info)

    else:
        print(f"Failed to download HTML code from {url}")

# Save combined book information to a CSV file
csv_file = "book_info.csv"

with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(
        ["Title", "Author", "Average Rating", "Ratings Count", "Cover Image URL"]
    )

    for book_info in book_info_list:
        csv_writer.writerow(
            [
                book_info.get("title", ""),
                book_info.get("author", ""),
                book_info.get("average_rating", ""),
                book_info.get("ratings_count", ""),
                book_info.get("cover_image_url", ""),
            ]
        )

print(f"Combined book information has been saved to {csv_file}")
