import logging
from requests_cache import CachedSession
from bs4 import BeautifulSoup

logging.basicConfig()
logger = logging.getLogger("SEARCH")
logger.setLevel(logging.DEBUG)

session = CachedSession(expire_after=3600)

SEARCH_BASE_URL = "https://www.mountainproject.com/ajax/public/search/results/overview"


def parse_user(user_html):
    soup = BeautifulSoup(user_html, "html.parser")
    user_id = soup.find("a")["href"].split("/")[2]
    img_url = soup.find("img")["src"]
    divs = soup.select("div")
    name = divs[0].text
    location = divs[1].text
    return {"userId": user_id, "imgUrl": img_url, "name": name, "location": location}


def get_user_search_results(user_query):
    search_response = session.get(SEARCH_BASE_URL + "?q=" + user_query)  # verify=False
    search_results = search_response.json()["results"]

    try:
        user_results = search_results["Users"]
        return [parse_user(user) for user in user_results]
    except KeyError:
        logging.info("No users found")
