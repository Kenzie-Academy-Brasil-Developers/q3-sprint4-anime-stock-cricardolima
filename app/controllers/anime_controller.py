from flask import jsonify, request
from http import HTTPStatus
from app.models.anime_model import Anime
from psycopg2.errors import UniqueViolation

def get_animes():
    animes = Anime.get_all()
    animes_list = Anime.serialize_anime(animes)
    
    return jsonify({"data": animes_list}), HTTPStatus.OK

def create_anime():
    data = request.get_json()
    try:
        anime = Anime(**data)
        created_anime = anime.create_anime()
    except KeyError:
        valid_keys = ["anime", "released_date", "seasons"]
        wrong_field = [key for key in data.keys() if key not in valid_keys]
        return {"allowed_fields": valid_keys, "wrong_fields_sended": wrong_field}, HTTPStatus.CONFLICT
    except UniqueViolation:
        return {"error": "anime already exists"}, HTTPStatus.UNPROCESSABLE_ENTITY
    created_anime = Anime.serialize_anime(created_anime)
    return jsonify(created_anime), HTTPStatus.CREATED