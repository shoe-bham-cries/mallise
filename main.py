import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv
import os
import html

load_dotenv()

# SET ANY VALUE HERE
CUTOFF_PRICE = 1000


headers = {
            'Accept-Language': "en-US,en;q=0.5",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
}
URL = "https://www.amazon.in/Snazzy-Foldable-Bookshelf-Bookshelves-Bookrack/dp/B09MT7KV4R/ref=sr_1_12?keywords=book+shelf&qid=1655155280&sprefix=book+sh%2Caps%2C294&sr=8-12"
my_email = os.getenv('email')
password = os.getenv('password')
recipient = os.getenv('recipient')
response = requests.get(url=URL, headers=headers).text


soup = BeautifulSoup(response, "html.parser")
object = soup.find(id="productTitle").getText()
current_price = float(soup.find("span", class_="a-price-whole").getText()+soup.find("span", class_="a-price-fraction").getText())
cutoff_price = CUTOFF_PRICE
message = f"The price of the object: {object} has reduced to ₹{current_price}, go buy immediately!"
if current_price < cutoff_price:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=recipient,
            msg=f"Subject: Price Update from Amazon\n\n{message.encode('utf8')}"
        )
        print("Done!")
else:
    print("cutoff not met! :(")