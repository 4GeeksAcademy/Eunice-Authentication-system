"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
from api.models import db, User
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands

# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../public/")
app = Flask(__name__)
app.url_map.strict_slashes = False

bcrypt = Bcrypt(app)

app.config["JWT_SECRET_KEY"] = os.environ.get('JWS_SECRET')
jwt = JWTManager(app)

# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

# Allow CORS requests to this API
CORS(app)

# add the admin
setup_admin(app)

# add the admin
setup_commands(app)

# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix="/api")

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route("/")
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, "index.html")

# any other endpoint will try to serve it like a static file


@app.route("/<path:path>", methods=["GET"])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = "index.html"
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response


@app.route("/signin", methods=["POST"])
def post_user():
    request_body = request.get_json(silent=True)

    if request_body is None:
        raise APIException("You must send information", 400)
    if "username" not in request_body:
        raise APIException("Username is required", 404)
    if "email" not in request_body:
        raise APIException("Email is required", 404)
    if "password" not in request_body:
        raise APIException("Password is required", 404)

    duplicate_username = User.query.filter_by(
        username=request_body["username"]).first()
    duplicate_email = User.query.filter_by(
        email=request_body["email"]).first()

    if duplicate_username:
        raise APIException("Username already exists", 400)
    if duplicate_email:
        raise APIException("Email already exists", 400)

    pw_hash = bcrypt.generate_password_hash(
        request_body["password"]).decode("utf-8")

    user = User(
        username=request_body["username"],
        full_name=request_body["full_name"],
        email=request_body["email"],
        password=pw_hash
    )

    user.add()
    return jsonify({"User created successfully"}), 201


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        raise APIException("Invalid user", status_code=400)

    user.delete()

    return jsonify({"User deleted successfully"}), 200


@app.route("/login", methods=["POST"])
def login():
    request_body = request.get_json(silent=True)
    if request_body is None:
        raise APIException("You must send information", 400)
    if "email" not in request_body:
        raise APIException("Email is required", 404)
    if "password" not in request_body:
        raise APIException("Password is required", 404)

    user_data = User.query.filter_by(email=request_body["email"]).first()

    if user_data is None:
        raise APIException("Invalid user", status_code=400)
    if user_data.password != request_body["password"]:
        raise APIException("Invalid password", status_code=400)

    access_token = create_access_token(identity=request_body["email"])

    return jsonify(access_token=access_token), 200


@app.route("/locked", methods=["GET"])
@jwt_required()
def locked():
    identity = get_jwt_identity()
    return jsonify({"msg": "Token approved sucessfully", "identity": identity}), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3001))
    app.run(host="0.0.0.0", port=PORT, debug=True)
