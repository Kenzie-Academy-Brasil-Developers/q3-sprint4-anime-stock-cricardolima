from flask import Blueprint, Flask

from app.routes.anime_route import bp as bp_animes 

bp_api = Blueprint("", __name__, url_prefix="/")

def init_app(app: Flask):
    
    bp_api.register_blueprint(bp_animes)
    
    app.register_blueprint(bp_api)