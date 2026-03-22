from flask import jsonify

from app.database.databaseControl import (
    GetPendingPlayersDB,
    insertScoreDB,
    updateNameDB,
    searchPlayersDB
)


def insertScore(data):
    if "score_player" not in data:
        return jsonify({"status": "score_player not exist"}), 400

    try:
        score_player = int(data["score_player"])
    except (TypeError, ValueError):
        return jsonify({"status": "invalid_score"}), 400

    if score_player < 0:
        return jsonify({"status": "invalid_score"}), 400

    idPending = GetPendingPlayersDB()
    if len(idPending) >= 1:
        return jsonify({"status": "pause", "pending": idPending}), 409

    insertScoreDB(score_player)
    return jsonify({"status": "ok"}), 200



def insertUsername(data):
    if "username" not in data:
        return jsonify({"status": "username not exist"}), 400

    username = str(data["username"]).strip()
    if username == "":
        return jsonify({"status": "invalid_username"}), 400

    idPending = GetPendingPlayersDB()
    if idPending == []:
        return jsonify({"status": "notPending"}), 404

    idMin = min(idPending)
    updateNameDB(idMin, username)
    return jsonify({"status": "ok", "player_id": idMin}), 200



def searchPeding():
    idPending = GetPendingPlayersDB()
    return jsonify({"pending": [pid for pid in idPending]}), 200



def rankingGenerate():
    return jsonify(searchPlayersDB()), 200
