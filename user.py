import logging
from requests_cache import CachedSession
from bs4 import BeautifulSoup

logging.basicConfig()
logger = logging.getLogger("SEARCH")
logger.setLevel(logging.DEBUG)

session = CachedSession(expire_after=3600)

USER_BASE_URL = "https://www.mountainproject.com/user"


def parse_user(profile_html):
    soup = BeautifulSoup(profile_html, "html.parser")
    img_url = soup.find_all("div", class_="user-img-avatar")[0]["data-original"]
    user_info_div = soup.find("div", id="user-info")
    first_row_in_user_info_div = user_info_div.div
    first_level_info_div = first_row_in_user_info_div.find_all("div")[2]
    name = first_level_info_div.h2.text
    location = first_level_info_div.div.contents[0].strip()
    return {"imgUrl": img_url, "name": name, "location": location}


def get_user(userid_username):
    page = session.get(USER_BASE_URL + f"/{userid_username}")
    return parse_user(page.text)
    
