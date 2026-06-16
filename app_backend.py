import os
import json
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5500,http://127.0.0.1:5500"
).split(",")

CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}})

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
LOGIN_TABLE_NAME = os.getenv("LOGIN_TABLE_NAME", "login")
MUSIC_TABLE_NAME = os.getenv("MUSIC_TABLE_NAME", "music")
SUBSCRIPTIONS_TABLE_NAME = os.getenv("SUBSCRIPTIONS_TABLE_NAME", "subscriptions")

# boto3 reads credentials from environment variables, AWS CLI profile, IAM role, or ECS task role.
# Do not hardcode AWS keys in this file.
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

login_table = dynamodb.Table(LOGIN_TABLE_NAME)
music_table = dynamodb.Table(MUSIC_TABLE_NAME)
subscriptions_table = dynamodb.Table(SUBSCRIPTIONS_TABLE_NAME)


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError


def json_response(data, status=200):
    return app.response_class(
        response=json.dumps(data, default=decimal_default),
        status=status,
        mimetype="application/json"
    )


@app.route("/")
def home():
    return jsonify({"message": "Music backend running"})


# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
@app.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"success": False, "message": "email or password is invalid"}), 400

    res = login_table.get_item(Key={"email": email})
    user = res.get("Item")

    stored_password_hash = user.get("password_hash", "") if user else ""

    if not user or not check_password_hash(stored_password_hash, password):
        return jsonify({"success": False, "message": "email or password is invalid"}), 401

    return json_response({
        "success": True,
        "email": user.get("email"),
        "user_name": user.get("user_name")
    })


# ─────────────────────────────────────────────
# REGISTER
# ─────────────────────────────────────────────
@app.route("/register", methods=["POST"])
def register():
    data = request.json or {}
    email = data.get("email", "").strip().lower()
    user_name = data.get("user_name", "").strip()
    password = data.get("password", "")

    if not email or not user_name or not password:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    existing = login_table.get_item(Key={"email": email})
    if "Item" in existing:
        return jsonify({"success": False, "message": "The email already exists"}), 409

    login_table.put_item(Item={
        "email": email,
        "user_name": user_name,
        "password_hash": generate_password_hash(password)
    })

    return jsonify({"success": True, "message": "Registered successfully"})


# ─────────────────────────────────────────────
# MUSIC QUERY
# Uses GSI when album + year are provided.
# Falls back to Scan when query pattern is broader.
# ─────────────────────────────────────────────
@app.route("/music", methods=["GET"])
def music():
    title = request.args.get("title", "").strip()
    artist = request.args.get("artist", "").strip()
    year = request.args.get("year", "").strip()
    album = request.args.get("album", "").strip()

    title_l = title.lower()
    artist_l = artist.lower()
    year_l = year.lower()
    album_l = album.lower()

    # Efficient Query using GSI: album-year-index
    if album and year:
        try:
            res = music_table.query(
                IndexName="album-year-index",
                KeyConditionExpression=Key("album").eq(album) & Key("year").eq(year)
            )
            items = res.get("Items", [])
        except Exception:
            items = []

        # fallback for case mismatch, e.g. user types "fearless" instead of "Fearless"
        if not items:
            res = music_table.scan(
                FilterExpression=Attr("album").contains(album) & Attr("year").contains(year)
            )
            items = res.get("Items", [])

    # Efficient Query using main table key when artist is provided
    elif artist:
        try:
            res = music_table.query(
                KeyConditionExpression=Key("artist").eq(artist)
            )
            items = res.get("Items", [])
        except Exception:
            items = []

        # fallback for case mismatch
        if not items:
            res = music_table.scan()
            items = res.get("Items", [])

    # General fallback scan for flexible multi-field searching
    else:
        res = music_table.scan()
        items = res.get("Items", [])

    filtered = []

    for song in items:
        song_title = str(song.get("title", "")).lower()
        song_artist = str(song.get("artist", "")).lower()
        song_year = str(song.get("year", "")).lower()
        song_album = str(song.get("album", "")).lower()

        if title_l and title_l not in song_title:
            continue
        if artist_l and artist_l not in song_artist:
            continue
        if year_l and year_l not in song_year:
            continue
        if album_l and album_l not in song_album:
            continue

        filtered.append(song)

    return json_response(filtered)


# ─────────────────────────────────────────────
# GET SUBSCRIPTIONS
# ─────────────────────────────────────────────
@app.route("/subscribe", methods=["GET"])
def get_subscriptions():
    email = request.args.get("email", "").strip().lower()

    if not email:
        return jsonify({"success": False, "message": "Missing email"}), 400

    res = subscriptions_table.query(
        KeyConditionExpression=Key("email").eq(email)
    )

    return json_response(res.get("Items", []))


# ─────────────────────────────────────────────
# ADD SUBSCRIPTION
# ─────────────────────────────────────────────
@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json or {}

    email = data.get("email", "").strip().lower()
    title = data.get("title")
    artist = data.get("artist")
    year = data.get("year")
    album = data.get("album")
    image_url = data.get("image_url")

    if not email or not title or not artist:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    song_id = data.get("song_id") or f"{artist}#{title}#{album}#{year}"

    existing = subscriptions_table.get_item(
        Key={"email": email, "song_id": song_id}
    )

    if "Item" in existing:
        return jsonify({"success": False, "message": "Already subscribed"}), 409

    subscriptions_table.put_item(Item={
        "email": email,
        "song_id": song_id,
        "title": title,
        "artist": artist,
        "year": year,
        "album": album,
        "image_url": image_url
    })

    return jsonify({"success": True, "message": "Subscribed successfully"})


# ─────────────────────────────────────────────
# REMOVE SUBSCRIPTION
# ─────────────────────────────────────────────
@app.route("/subscribe", methods=["DELETE"])
def remove_subscription():
    data = request.json or {}

    email = data.get("email", "").strip().lower()
    song_id = data.get("song_id")

    if not email or not song_id:
        return jsonify({"success": False, "message": "Missing email or song_id"}), 400

    subscriptions_table.delete_item(
        Key={"email": email, "song_id": song_id}
    )

    return jsonify({"success": True, "message": "Removed successfully"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG") == "1")
