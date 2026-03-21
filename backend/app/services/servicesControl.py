from flask import request, jsonify
from app.database.databaseControl import GetPendingPlayersDB, insertScoreDB, updateNameDB, searchPlayersDB

def insertScore(data):
    if 'score_player' not in data:
        return jsonify({'status':'score_player not exist'}), 400

    score_player = data['score_player']
    idPending = GetPendingPlayersDB()

    if len(idPending) >= 1:
        print('esperando username')
        return jsonify({'status':'pause'})
    else:
        insertScoreDB(score_player)
        return jsonify({'status':'ok'})

def insertUsername(data):
    if 'username' not in data:
        return jsonify({'status':'username not exist'}), 400

    username = data['username']
    idPending = GetPendingPlayersDB()

    if idPending != []:
        idmax = min(idPending)
    else:
        return jsonify({'status':'notPeding'})

    updateNameDB(idmax, username)

    return jsonify({'status':'ok'})

def searchPeding():
    idPending = GetPendingPlayersDB()  

    if idPending:  
        return jsonify({'pending': [pid for pid in idPending]}), 200
    else:
        return jsonify({'pending': []}), 200 

def rankingGenerate(): return jsonify(searchPlayersDB()), 200