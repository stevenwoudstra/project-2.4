from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, get_jwt
)
from datetime import datetime, timedelta, timezone

from app import app
from app.utils import init_routing_func, check_request_data
from app.obj_utils import get_objs, get_objs_with_filter, create_obj
from database.tables import User, Game, TopScore, UserGame

memory_api, get, post = init_routing_func('memory_api', '/wmsdemo/')

@get('/games')
def getGames():
    games=get_objs(Game, relations=True)
    return jsonify(games),200

@get('/users')
def getUsers():
    users=get_objs(User, relations=True)
    return jsonify(users),200

@get('/topscores')
def getTopscores():
    topscores=get_objs(TopScore, relations=True)
    return jsonify(topscores)

@get('/topscores/game/<int:game_id>')
def getTopscoresGame(game_id):
    topscores=get_objs_with_filter(TopScore, relations=True, game_id=game_id)
    return jsonify(topscores)

@post('/user')
def saveUser():
    data = request.json
    message, response_code = check_request_data(data, ["user_name", "user_age"])
    if (response_code == 200):
        newUser = create_obj(User, data)
        message = jsonify(newUser.to_dict())
    return message, response_code
