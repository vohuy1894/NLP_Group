import requests
import re
from bs4 import BeautifulSoup

URL = "https://www.gutenberg.org/browse/scores/top"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
top_100_list = soup.find_all("ol")[0]
#print(top_100_list.prettify())

book_links = top_100_list.find_all("a")
book_numbers = []
for book_link in book_links:
    book_numbers.append(book_link['href'].split('/')[-1])
    
BASE_BOOK_URL_PREFIX = "https://www.gutenberg.org/files/"
BASE_BOOK_URL_SUFFIX = "-0.txt"

for book_number in book_numbers:
    print(book_number)
    BOOK_URL = BASE_BOOK_URL_PREFIX + book_number + "/" + book_number + BASE_BOOK_URL_SUFFIX
    book_page = requests.get(BOOK_URL)
    
    body_text = BeautifulSoup(book_page.content, "html.parser").prettify()
    body_text = str(body_text.encode('utf8'))
    body = re.split(r'\*{3}[^\*]*\*{3}', body_text)
    
    if len(body)>1:
        body = body[1]
    else:
        body = body[0]
    
    file = open('book text/'+book_number+".txt", "a+")
    file.write(body)
    file.close()
    