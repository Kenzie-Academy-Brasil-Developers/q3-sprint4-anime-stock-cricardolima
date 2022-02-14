from flask import jsonify, request
from http import HTTPStatus
from app.models.anime_model import Anime
from psycopg2.errors import UndefinedColumn, UniqueViolation

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

def get_by_id(id):
    anime = Anime.get_by_id(id)
    if anime is None:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    returned_anime = Anime.serialize_anime(anime)
    return jsonify({"data": returned_anime}), HTTPStatus.OK

def update_anime(id):
    data = request.get_json()
    try:
        updated_anime = Anime.update_anime(id, data)
    except KeyError:
        valid_keys = ["anime", "released_date", "seasons"]
        wrong_field = [key for key in data.keys() if key not in valid_keys]
        return {"allowed_fields": valid_keys, "wrong_fields_sended": wrong_field}, HTTPStatus.CONFLICT
    except UndefinedColumn:
        return {"error": "Not Found"}, HTTPStatus.UNPROCESSABLE_ENTITY
    updated_anime = Anime.serialize_anime(updated_anime)
    
    return jsonify(updated_anime), HTTPStatus.OK

def delete_anime(id):
    deleted_anime = Anime.delete_anime(id)
    if not deleted_anime:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    delete_anime = Anime.serialize_anime(deleted_anime)
    return jsonify(None), HTTPStatus.NO_CONTENT