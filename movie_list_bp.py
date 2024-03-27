from flask import Blueprint, request, render_template
from app import Movie, db

movies_list_bp = Blueprint("movies_list", __name__)


@movies_list_bp.route("/")
def movie_list():
    movie_list = Movie.query.all()
    data = [movie.to_dict() for movie in movie_list]
    return render_template("movie-list.html", movies=data)


@movies_list_bp.route("/<id>")
def display_specific_movie(id):
    filtered_movie = Movie.query.get(id)
    if filtered_movie is None:
        return "<h1>404 Movie Not Found</h2>"
    data = filtered_movie.to_dict()
    return render_template("movie-detail.html", movie=data)


@movies_list_bp.route("/delete", methods=["POST"])  # HOF
def delete_movie_by_id():
    id = request.form.get("movie_id")
    filtered_movie = Movie.query.get(id)
    if filtered_movie is None:
        return "<h2>404 Movie not found</h2>"
    try:
        data = filtered_movie.to_dict()
        db.session.delete(filtered_movie)
        db.session.commit()
        return f"<h2>{data['name']} Deleted Successfully</h2>"
    except Exception as e:
        db.session.rollback()
        return "<h2>Error Occurred</h2>"


@movies_list_bp.route("/add", methods=["GET"])
def add_movie_form():
    return render_template("add_movie.html")


@movies_list_bp.route("/added", methods=["POST"])
def movie_form_values():
    data = {
        "name": request.form.get("name"),
        "poster": request.form.get("poster"),
        "rating": request.form.get("rating"),
        "summary": request.form.get("summary"),
        "trailer": request.form.get("trailer"),
    }
    try:
        new_movie = Movie(**data)
        db.session.add(new_movie)
        db.session.commit()
        return f"<h2>{data['name']} Added Successfully</h2>"
    except Exception as e:
        db.session.rollback()
        return "<h2>Error Occurred</h2>"


@movies_list_bp.route("/update", methods=["GET"])
def update_movie_form():
    movie_list = Movie.query.all()
    data = [movie.to_dict() for movie in movie_list]
    return render_template("update-movie.html", movies=data)


@movies_list_bp.route("/updated", methods=["POST"])
def update_movie_result():
    movie_id = request.form.get("movie_id")
    return f"<h2>{movie_id}</h2>"
