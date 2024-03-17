from flask import Blueprint
from flask_restx import Api
from api.auth import auth_api
from api.movie import movie_api

blueprint = Blueprint("api","User api")
api = Api(blueprint,title='Apis',version="1.0",description="Api")

api.add_namespace(auth_api)
api.add_namespace(movie_api)