from flask import Blueprint, request, jsonify, redirect
from app.utils import generate_code, is_valid_url
from app.models import url_store
from datetime import datetime

url_routes = Blueprint("url_routes", __name__)

# Shorten URL Endpoint
@url_routes.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    long_url = data.get("url")

    if not long_url or not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = generate_code()
    while short_code in url_store:
        short_code = generate_code()

    url_store[short_code] = {
        "url": long_url,
        "clicks": 0,
        "created_at": datetime.utcnow()
    }

    return jsonify({
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}"
    })

# Redirect Endpoint
@url_routes.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    data = url_store.get(short_code)
    if not data:
        return jsonify({"error": "Short code not found"}), 404

    data["clicks"] += 1
    return redirect(data["url"])

# Analytics Endpoint
@url_routes.route("/api/stats/<short_code>", methods=["GET"])
def get_stats(short_code):
    data = url_store.get(short_code)
    if not data:
        return jsonify({"error": "Short code not found"}), 404

    return jsonify({
        "url": data["url"],
        "clicks": data["clicks"],
        "created_at": data["created_at"].isoformat()
    })
