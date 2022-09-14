from typing import Dict, Tuple, Any, List
from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema, Genre
from decorator import auth_required, admin_required
from implemented import genre_service

genre_ns: Namespace = Namespace('genres')

genre_schema: GenreSchema = GenreSchema()
genres_schema: GenreSchema = GenreSchema(many=True)


@genre_ns.route('/')
class GenresView(Resource):

    @auth_required
    def get(self) -> Tuple[List[Dict[str, Any]], int]:

        if 'page' in request.args:
            genres = genre_service.get_all(request.args['page'])
        else:
            genres: List[Genre] = genre_service.get_all()
        return genres_schema.dump(genres), 200

    @admin_required
    def post(self) -> Tuple[str, int, Dict[str, str]]:
        req_json: Dict[str, Any] = request.json
        genre: Genre = genre_service.create(req_json)
        return "", 201, {"location": f"/genres/{genre.id}"}


@genre_ns.route('/<int:gid>/')
class GenreView(Resource):

    @auth_required
    def get(self, gid: int) -> Tuple[Dict[str, Any], int]:
        genre: Genre = genre_service.get_one(gid)
        return genre_schema.dump(genre), 200

    @admin_required
    def put(self, gid: int) -> Tuple[str, int]:
        req_json: Dict[str, Any] = request.json
        genre_service.update(gid, req_json)
        return "", 204

    @admin_required
    def delete(self, gid: int) -> Tuple[str, int]:
        genre_service.delete(gid)
        return "", 204
