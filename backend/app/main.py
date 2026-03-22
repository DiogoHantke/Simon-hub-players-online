import os
import sys
from flask import Flask, render_template, request, jsonify

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.database.databaseControl import createTables
from app.services.servicesControl import insertScore, insertUsername, searchPeding, rankingGenerate

app = Flask(__name__)

createTables()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/score", methods=["POST"])
def score():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "invalid_json"}), 400
    if "score_player" not in data:
        return jsonify({"status": "score_player not exist"}), 400
    return insertScore(data)


@app.route("/username", methods=["POST"])
def username():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "invalid_json"}), 400
    if "username" not in data:
        return jsonify({"status": "username not exist"}), 400
    return insertUsername(data)


@app.route("/search", methods=["GET"])
def search():
    return searchPeding()


@app.route("/ranking", methods=["GET"])
def ranking():
    return rankingGenerate()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
