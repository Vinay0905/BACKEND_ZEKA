import requests
from bs4 import BeautifulSoup

url = input("Enter the URL to scrape: ")

def ensure_https(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url

url = ensure_https(url)

def scrape():
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print(soup)

    with open("example.txt", "w", encoding="utf-8") as file:
        file.write(str(soup))

if __name__ == '__main__':
    scrape()