import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_wikipedia():
    url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "wikitable"})
    df = pd.read_html(str(table))[0]
    df.columns = [col[1] if isinstance(col, tuple) else col for col in df.columns]
    return df
