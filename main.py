from flask import Flask, render_template, request, jsonify
from app.database.databaseControl import createTables
from app.services.servicesControl import insertScore, insertUsername, searchPeding, rankingGenerate

app = Flask(__name__)

createTables()

@app.route("/", methods=['GET'])
def home(): return render_template("index.html")

@app.route("/score", methods=["POST"])
def score(): 
    data = request.json

    if 'score_player' not in data:
        return jsonify({'status':'score_player not exist'}), 400

    if data is None or data == {}:
        return jsonify({'status':'invalid_json'}), 400

    return insertScore(data)

@app.route("/username", methods=["POST"])
def username(): 
    data = request.json

    if 'username' not in data:
        return jsonify({'status':'username not exist'}), 400

    if data is None or data == {}:
        return jsonify({'status':'invalid_json'}), 400

    return insertUsername(data)

@app.route("/search", methods=["GET"])
def search(): return searchPeding()

@app.route("/ranking", methods=["GET"])
def ranking(): return rankingGenerate()
    
if __name__ == "__main__":
    app.run(debug=True)