import importlib
import glob

from pathlib import Path
from os.path import dirname, basename, isfile, join
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import config
from src.schemas.base import db
from src.modules.redis import red

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = config["JWT_SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config["JWT_EXPIRES"]
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = config["JWT_REFRESH_EXPIRES"]

jwt = JWTManager(app)
CORS(app, supports_credentials=True)

route_path = Path(dirname(__file__) + "/src/routes").resolve()
routes = [basename(f)[:-3] for f in glob.glob(join(route_path, "*.py")) if isfile(f)]

for route in routes:
    module = importlib.import_module(f"src.routes.{route}")
    app.register_blueprint(module.bl, url_prefix=f"/{route}")


@app.before_request
def open_connection():
    db.connect()


@app.teardown_request
def close_connection(exc):
    db.close()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"msg": "Not found", "status": 404}), 404


@app.errorhandler(500)
def page_bad(e):
    return jsonify({"msg": "Internal server error", "status": 500}), 500


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return identity


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token_in_redis = red.get(jti)
    return token_in_redis is not None


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
