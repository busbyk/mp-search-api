import logging
from flask import Flask, json, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from search import get_user_search_results
from ticks import get_user_ticks
from user import get_user

logging.basicConfig()
logger = logging.getLogger("APP")
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["300 per day", "50 per hour", "20 per minute"],
)
CORS(app)


@app.route("/")
@limiter.exempt
def index():
    return "Welcome to an API for the Mountain Project user search"


@app.route("/userSearch")
def user_search():
    user_query = request.args.get("userQuery")
    results = get_user_search_results(user_query)
    return jsonify(results)


@app.route("/userTicks")
def user_ticks():
    user = request.args.get("user")
    ticks = get_user_ticks(user)
    return jsonify(ticks)


@app.route("/userInfo")
def user_info():
    userid_username = request.args.get("user")
    user = get_user(userid_username)
    return jsonify(user)


@app.route("/ping")
def ping():
    return "pong"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
