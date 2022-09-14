from typing import Dict, Tuple, Any, Optional, Union

from flask import request
from flask_restx import Namespace, Resource

from dao.model.user import User
from implemented import auth_service, user_service

auth_ns: Namespace = Namespace('auth')


@auth_ns.route('/login/')
class AuthView(Resource):

    def post(self) -> Tuple[Union[Dict[str, str], str], int]:
        data: Dict[str, Any] = request.json

        email: Optional[str] = data.get('email', None)
        password: Optional[str] = data.get('password', None)

        if None in [email, password]:
            return '', 401

        return auth_service.generate_tokens(email, password), 200

    def put(self) -> Tuple[Dict[str, str], int]:
        data: Dict[str, Any] = request.json

        token: str = data.get('refresh_token')
        return auth_service.approve_refresh_taken(token), 200


@auth_ns.route('/register/')
class AuthRegisterView(Resource):

    def post(self) -> Tuple[str, int, Dict[str, str]]:
        req_json: Dict[str, Any] = request.json

        email: Optional[str] = req_json.get('email', None)
        password: Optional[str] = req_json.get('password', None)

        if None in [email, password]:
            return '', 401, {}

        user: User = user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}
