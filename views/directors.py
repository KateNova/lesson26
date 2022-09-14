from typing import Dict, Tuple, Any, List

from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema, Director
from decorator import auth_required, admin_required
from implemented import director_service

director_ns: Namespace = Namespace('directors')

director_schema: DirectorSchema = DirectorSchema()
directors_schema: DirectorSchema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):

    @auth_required
    def get(self) -> Tuple[List[Dict[str, Any]], int]:
        if 'page' in request.args:
            directors = director_service.get_all(request.args['page'])
        else:
            directors: List[Director] = director_service.get_all()
        return directors_schema.dump(directors), 200

    @admin_required
    def post(self) -> Tuple[str, int, Dict[str, str]]:
        req_json: Dict[str, Any] = request.json
        director: Director = director_service.create(req_json)
        return "", 201, {"location": f"/directors/{director.id}"}


@director_ns.route('/<int:did>/')
class DirectorView(Resource):

    @auth_required
    def get(self, did: int) -> Tuple[Dict[str, Any], int]:
        director: Director = director_service.get_one(did)
        return director_schema.dump(director), 200

    @admin_required
    def put(self, did: int) -> Tuple[str, int]:
        req_json: Dict[str, Any] = request.json
        director_service.update(did, req_json)
        return "", 204

    @admin_required
    def delete(self, did: int) -> Tuple[str, int]:
        director_service.delete(did)
        return "", 204
