from flask import Blueprint, jsonify, request, current_app
from app import Movie, db

# import uuid
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()


movies_bp = Blueprint("movies", __name__)


# /movies --> JSON
@movies_bp.get("/")
def get_movies():
    movie_list = Movie.query.all()  # Select * from movies
    data = [
        movie.to_dict() for movie in movie_list
    ]  # Converting into list of dictionaries
    return jsonify(data)


# Generator expression
@movies_bp.get("/<id>")
def get_specific_movie(id):
    filtered_movie = Movie.query.get(id)
    if filtered_movie is None:
        return jsonify({"message": "Movie Not found"}), 404
    return jsonify(filtered_movie.to_dict())


@movies_bp.post("/")
def add_movies():
    data = request.json

    # new_movie = Movie(
    #     name=data["name"],
    #     poster=data["poster"],
    #     rating=data["rating"],
    #     summary=data["summary"],
    #     trailer=data["trailer"],
    # )
    new_movie = Movie(**data)
    try:
        db.session.add(new_movie)
        db.session.commit()
        result = {"message": "added successfully", "data": new_movie.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@movies_bp.delete("/<id>")
def delete_movie(id):
    filtered_movie = Movie.query.get(id)
    if filtered_movie is None:
        return jsonify({"message": "Movie Not found"}), 404
    try:
        data = filtered_movie.to_dict()
        db.session.delete(filtered_movie)
        db.session.commit()
        return jsonify(data)
    except Exception as e:
        db.session.rollback()  # undo the commit
        return {"message": str(e)}, 500


@movies_bp.put("/<id>")
def update_movies(id):
    movie_update = request.json
    filtered_movie = Movie.query.get(id)
    if filtered_movie is None:
        return jsonify({"message": "Movie Not found"}), 404
    try:
        for key, value in movie_update.items():
            if hasattr(filtered_movie, key):
                setattr(filtered_movie, key, value)

        # filtered_movie.name = movie_update.get("name", filtered_movie.name)
        # filtered_movie.rating = movie_update.get("rating", filtered_movie.rating)
        # filtered_movie.poster = movie_update.get("poster", filtered_movie.poster)
        # filtered_movie.summary = movie_update.get("summary", filtered_movie.summary)
        # filtered_movie.trailer = movie_update.get("trailer", filtered_movie.trailer)
        db.session.commit()
        result = {"message": "updated successfully", "data": filtered_movie.to_dict()}
        return jsonify(result)
    except Exception as e:
        db.session.rollback()
        return {"message": str(e)}, 500
