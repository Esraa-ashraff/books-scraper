from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

all_books = []
rating_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

url = "https://books.toscrape.com/catalogue/page-1.html"

while url:
    response = requests.get(url)
    soup = bs(response.text,'html.parser')

    
    books = soup.find_all("article", class_="product_pod")
    for b in books:
        title = b.h3.a["title"]
        
        price = float(
            b.find("p", class_="price_color")
            .text.replace("£", "")
            .replace("Â", "")
        )
        
        rating_word = b.find("p", class_="star-rating")["class"][1]
        rating = rating_dict[rating_word]
        
        stock_text = b.find("p", class_="instock availability").text.strip()
        in_stock = "In stock" in stock_text

        book_url = b.h3.a["href"]

        all_books.append(
            {
                "title": title,
                "price": price,
                "rating": rating,
                "in_stock": in_stock,
                "url": "https://books.toscrape.com/catalogue/"+book_url,
            }
        )

    pager = soup.find("li", class_="current")
    if pager and "Page 5" in pager.text:
        break


    next_button = soup.find("li", class_="next")
    if next_button:
        next_href = next_button.a["href"]
        url = "https://books.toscrape.com/catalogue/"+ next_href
    else:
        break


df = pd.DataFrame(all_books)
print(df)
df.to_csv("books.csv", index=False, encoding="utf-8")
