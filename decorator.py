from flask import request
from flask_restx import abort
import jwt

from config import Config


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, Config.JWT_SECRET, algorithms=Config.JWT_ALGO)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            user = jwt.decode(token, Config.JWT_SECRET, algorithms=Config.JWT_ALGO)
            role = user.get('role')
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        if role != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return wrapper


def user_identification(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            user = jwt.decode(token, Config.JWT_SECRET, algorithms=Config.JWT_ALGO)
            email = user.get('email')
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        if not email:
            abort(403)

        return func(*args, **kwargs, email=email)

    return wrapper
