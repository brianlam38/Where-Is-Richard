from flask_boilerplate_utils.overrides import NestableBlueprint
from flask.ext import menu
from flask_menu.classy import register_flaskview

frontend = NestableBlueprint('frontend', __name__, template_folder="templates", 
    static_folder="static")

from .controllers.Index import Index
Index.register(frontend)
register_flaskview(frontend, Index)

