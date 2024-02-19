from os import environ

from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


def json(self):
    return {"id": self.id, "username": self.username, "email": self.email}


db.create_all()


@app.route("/test", methods=["GET"])
def test():
    return make_response(jsonify({"status": "ok"}), 200)


# create a user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data:
        return make_response(
            jsonify({"status": "error", "data": "No input data provided"}), 400
        )
    # check the required fields
    if "username" not in data or "email" not in data:
        return make_response(
            jsonify({"status": "error", "data": "Missing username or email"}), 400
        )
    try:
        user = User(username=data["username"], email=data["email"])
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({"status": "ok", "data": user.json()}), 201)
    except Exception as e:
        return make_response(jsonify({"status": "error", "data": str(e)}), 400)


# get all users
@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        return make_response(
            jsonify({"status": "ok", "data": [user.json() for user in users]}), 200
        )

    except Exception as e:
        return make_response(jsonify({"status": "error", "data": str(e)}), 400)


# get user by id
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return make_response(
                jsonify({"status": "error", "data": "User not found"}), 404
            )
        return make_response(jsonify({"status": "ok", "data": user.json()}), 200)
    except Exception as e:
        return make_response(jsonify({"status": "error", "data": str(e)}), 400)


# update user by id
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return make_response(
                jsonify({"status": "error", "data": "User not found"}), 404
            )
        data = request.get_json()
        if not data:
            return make_response(
                jsonify({"status": "error", "data": "No input data provided"}), 400
            )
        if "username" in data:
            user.username = data["username"]
        if "email" in data:
            user.email = data["email"]
        db.session.commit()
        return make_response(jsonify({"status": "ok", "data": user.json()}), 200)
    except Exception as e:
        return make_response(jsonify({"status": "error", "data": str(e)}), 400)


# delete a usere
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return make_response(
                jsonify({"status": "error", "data": "User not found"}), 404
            )
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"status": "ok", "data": user}), 200)
    except Exception as e:
        return make_response(jsonify({"status": "error", "data": str(e)}), 400)
