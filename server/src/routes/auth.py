from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user, create_access_token, get_jwt

from config import config
from src.modules.redis import red
from src.modules.auth import login_by_email, register_user
from src.schemas.base import db

bl = Blueprint("auth", __name__)


@bl.post("/token")
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if email is None and password is None:
        return jsonify({"msg": "Missing `email` or `password`", "status": 400}), 400

    user, error = login_by_email(email, password)

    if error:
        return jsonify({**error, "status": 400}), 400

    auth = user.pop("auth")
    refresh = user.pop("refresh")

    return jsonify({"user": user, "auth_token": auth, "refresh_token": refresh})


@bl.post("/register")
@db.atomic()
def register():
    email = request.json.get("email")
    password1 = request.json.get("password1")
    password2 = request.json.get("password2")

    if email is None and password1 is None:
        return jsonify({"msg": "Missing `email` or `password`", "status": 400}), 400

    if password1 != password2:
        return jsonify({"msg": "Passwords don't match", "status": 400}), 400

    user, error = register_user(email, password1)

    if error:
        return jsonify({**error, "status": 400}), 400

    auth = user.pop("auth")
    refresh = user.pop("refresh")

    return jsonify({"user": user, "auth_token": auth, "refresh_token": refresh})


@bl.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    return jsonify(
        auth_token=create_access_token(fresh=False, identity={**current_user})
    )


@bl.delete("/revoke")
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    red.set(jti, "", ex=config["JWT_EXPIRES"])
    return jsonify(msg="Access token revoked")


@bl.get("/me")
@jwt_required()
def me():
    return jsonify({"user": {**current_user}})
