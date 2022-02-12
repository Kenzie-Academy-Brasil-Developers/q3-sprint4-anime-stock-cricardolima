from flask import jsonify
from http import HTTPStatus
from app.models.anime_model import Anime

def get_animes():
    animes = Anime.get_all()
    animes_list = Anime.serialize_anime(animes)
    
    return jsonify({"data": animes_list}), HTTPStatus.OK