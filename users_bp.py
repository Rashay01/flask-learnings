from flask import Blueprint, request, render_template, jsonify
from sqlalchemy.sql import text
from sqlalchemy import select
from app import User, db

users_bp = Blueprint("users", __name__)


@users_bp.route("/login", methods=["GET"])
def forms_page():
    return render_template("forms.html")


@users_bp.route("/dashboard1", methods=["POST"])
def dashboard1_page():
    username = request.form.get("username")
    password = request.form.get("password")
    all_users = User.query.all()
    ans = [user.to_dict() for user in all_users]
    found_user = next(
        (
            user
            for user in ans
            if (user["username"] == username) and (user["password"] == password)
        ),
        None,
    )
    if found_user is None:
        return "<h2>Username and/or Password incorrect</h2>"
    print("Dashboard page", username, password)
    return render_template("dashboard1.html", username=username)


@users_bp.route("/sign-up", methods=["GET"])
def sign_up_page():
    return render_template("register.html")


@users_bp.route("/registered", methods=["POST"])
def sign_up_user():
    data = {
        "username": request.form.get("username"),
        "password": request.form.get("password"),
    }

    all_users = User.query.all()
    ans = [user.to_dict() for user in all_users]
    found_user = next(
        (user for user in ans if (user["username"] == data["username"])),
        None,
    )

    if found_user:
        return "<h2>Username already exists</h2>"
    new_user = User(**data)

    try:
        db.session.add(new_user)
        db.session.commit()
        return f"<h2>{data['username']} has been registered</h2>"
    except Exception as e:
        db.session.rollback()
        return "<h2>Error Occurred</h2>"


# @users_bp.route("/test")
# def testing():
#     test = User(username="Testing")
#     ans = User.query.where(User.username "Testing")
#     print(ans)
#     if ans is None:
#         return jsonify({"message": "No items"})
#     return jsonify({"message": True})
