import logging
from requests_cache import CachedSession
import csv

logging.basicConfig()
logger = logging.getLogger("TICKS")
logger.setLevel(logging.DEBUG)

session = CachedSession(expire_after=3600)

BASE_URL = "https://www.mountainproject.com/user/"
TICKS_ENDPOINT = "/tick-export"


def get_user_ticks(user_id):
    ticks_response = session.get(BASE_URL + user_id + TICKS_ENDPOINT)

    if ticks_response:
        decoded_content = ticks_response.content.decode("utf-8")
        cr = csv.DictReader(decoded_content.splitlines(), delimiter=",")
        ticks = list(cr)
        return ticks
    else:
        return {
            "error": f"Mountain project returned a {ticks_response.status_code} status code for user_id {user_id}"
        }
