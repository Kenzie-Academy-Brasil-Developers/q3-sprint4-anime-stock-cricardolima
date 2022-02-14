from flask import Blueprint
from app.controllers import anime_controller

bp = Blueprint("animes", __name__, url_prefix="/animes")

bp.get("")(anime_controller.get_animes)
bp.get("/<int:id>")(anime_controller.get_by_id)
bp.post("")(anime_controller.create_anime)
bp.patch("/<int:id>")(anime_controller.update_anime)
bp.delete("/<int:id>")(anime_controller.delete_anime)