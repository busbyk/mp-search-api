import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from search import get_user_search_results

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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
