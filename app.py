from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# local
movies = [
    {
        "id": "99",
        "name": "Vikram",
        "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
        "rating": 8.4,
        "summary": "Members of a black ops team must track and eliminate a gang of masked murderers.",
        "trailer": "https://www.youtube.com/embed/OKBMCL-frPU",
    },
    {
        "id": "100",
        "name": "RRR",
        "poster": "https://englishtribuneimages.blob.core.windows.net/gallary-content/2021/6/Desk/2021_6$largeimg_977224513.JPG",
        "rating": 8.8,
        "summary": "RRR is an upcoming Indian Telugu-language period action drama film directed by S. S. Rajamouli, and produced by D. V. V. Danayya of DVV Entertainments.",
        "trailer": "https://www.youtube.com/embed/f_vbAtFSEc0",
    },
    {
        "id": "101",
        "name": "Iron man 2",
        "poster": "https://m.media-amazon.com/images/M/MV5BMTM0MDgwNjMyMl5BMl5BanBnXkFtZTcwNTg3NzAzMw@@._V1_FMjpg_UX1000_.jpg",
        "rating": 7,
        "summary": "With the world now aware that he is Iron Man, billionaire inventor Tony Stark (Robert Downey Jr.) faces pressure from all sides to share his technology with the military. He is reluctant to divulge the secrets of his armored suit, fearing the information will fall into the wrong hands. With Pepper Potts (Gwyneth Paltrow) and Rhodes (Don Cheadle) by his side, Tony must forge new alliances and confront a powerful new enemy.",
        "trailer": "https://www.youtube.com/embed/wKtcmiifycU",
    },
    {
        "id": "102",
        "name": "No Country for Old Men",
        "poster": "https://upload.wikimedia.org/wikipedia/en/8/8b/No_Country_for_Old_Men_poster.jpg",
        "rating": 8.1,
        "summary": "A hunter's life takes a drastic turn when he discovers two million dollars while strolling through the aftermath of a drug deal. He is then pursued by a psychopathic killer who wants the money.",
        "trailer": "https://www.youtube.com/embed/38A__WT3-o0",
    },
    {
        "id": "103",
        "name": "Jai Bhim",
        "poster": "https://m.media-amazon.com/images/M/MV5BY2Y5ZWMwZDgtZDQxYy00Mjk0LThhY2YtMmU1MTRmMjVhMjRiXkEyXkFqcGdeQXVyMTI1NDEyNTM5._V1_FMjpg_UX1000_.jpg",
        "summary": "A tribal woman and a righteous lawyer battle in court to unravel the mystery around the disappearance of her husband, who was picked up the police on a false case",
        "rating": 8.8,
        "trailer": "https://www.youtube.com/embed/nnXpbTFrqXA",
    },
    {
        "id": "104",
        "name": "The Avengers",
        "rating": 8,
        "summary": "Marvel's The Avengers (classified under the name Marvel Avengers\n Assemble in the United Kingdom and Ireland), or simply The Avengers, is\n a 2012 American superhero film based on the Marvel Comics superhero team\n of the same name.",
        "poster": "https://terrigen-cdn-dev.marvel.com/content/prod/1x/avengersendgame_lob_crd_05.jpg",
        "trailer": "https://www.youtube.com/embed/eOrNdBpGMv8",
    },
    {
        "id": "105",
        "name": "Interstellar",
        "poster": "https://m.media-amazon.com/images/I/A1JVqNMI7UL._SL1500_.jpg",
        "rating": 8.6,
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\n of researchers, to find a new planet for humans.",
        "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E",
    },
    {
        "id": "106",
        "name": "Baahubali",
        "poster": "https://flxt.tmsimg.com/assets/p11546593_p_v10_af.jpg",
        "rating": 8,
        "summary": "In the kingdom of Mahishmati, Shivudu falls in love with a young warrior woman. While trying to woo her, he learns about the conflict-ridden past of his family and his true legacy.",
        "trailer": "https://www.youtube.com/embed/sOEg_YZQsTI",
    },
    {
        "id": "107",
        "name": "Ratatouille",
        "poster": "https://resizing.flixster.com/gL_JpWcD7sNHNYSwI1ff069Yyug=/ems.ZW1zLXByZC1hc3NldHMvbW92aWVzLzc4ZmJhZjZiLTEzNWMtNDIwOC1hYzU1LTgwZjE3ZjQzNTdiNy5qcGc=",
        "rating": 8,
        "summary": "Remy, a rat, aspires to become a renowned French chef. However, he fails to realise that people despise rodents and will never enjoy a meal cooked by him.",
        "trailer": "https://www.youtube.com/embed/NgsQ8mVkN8w",
    },
    {
        "name": "PS2",
        "poster": "https://m.media-amazon.com/images/M/MV5BYjFjMTQzY2EtZjQ5MC00NGUyLWJiYWMtZDI3MTQ1MGU4OGY2XkEyXkFqcGdeQXVyNDExMjcyMzA@._V1_.jpg",
        "summary": "Ponniyin Selvan: I is an upcoming Indian Tamil-language epic period action film directed by Mani Ratnam, who co-wrote it with Elango Kumaravel and B. Jeyamohan",
        "rating": 8,
        "trailer": "https://www.youtube.com/embed/KsH2LA8pCjo",
        "id": "108",
    },
    {
        "name": "Thor: Ragnarok",
        "poster": "https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_.jpg",
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\\n of researchers, to find a new planet for humans.",
        "rating": 8.8,
        "trailer": "https://youtu.be/NgsQ8mVkN8w",
        "id": "109",
    },
]

# jinja2 - templates
users = [
    {
        "name": "Dhara",
        "img": "https://i.pinimg.com/236x/db/b9/cb/dbb9cbe3b84da22c294f57cc7847977e.jpg",
        "pro": True,
    },
    {
        "name": "Arjun",
        "img": "https://images.unsplash.com/photo-1618641986557-1ecd230959aa?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8cHJvZmlsZXxlbnwwfHwwfHx8MA%3D%3D",
        "pro": False,
    },
    {
        "name": "John",
        "img": "https://imgv3.fotor.com/images/blog-richtext-image/10-profile-picture-ideas-to-make-you-stand-out.jpg",
        "pro": True,
    },
]


name = "Caleb"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming"]


@app.route("/")
def hello_world():
    return "<p>Super, Cool! 😁</p>"


@app.route("/about")
def about():
    return render_template("about.html", users=users)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", movies=movies)


@app.route("/profile")
def profile():
    return render_template("profile.html", name=name, hobbies=hobbies)


@app.route("/movie-list")
def movie_list():
    return render_template("movie-list.html", movies=movies)

@app.route("/movie-list/<id>")
def display_specific_movie(id):
    filtered_movie = next((movie for movie in movies if movie["id"] == id), None)
    if filtered_movie is None:
        return "<h1>404 Movie Not Found</h2>"
    return render_template("movie-detail.html", movie=filtered_movie)

@app.route("/login", methods=["GET"])
def forms_page():
    return render_template("forms.html")

# @app.route("/dashboard1", methods=["GET"])
# def dashboard1_page():
#     username = request.args.get("username")
#     password = request.args.get("password")
#     print("Dashboard page", username, password)
#     return render_template("dashboard1.html",username=username)

@app.route("/dashboard1", methods=["POST"])
def dashboard1_page():
    username = request.form.get("username")
    password = request.form.get("password")
    print("Dashboard page", username, password)
    return render_template("dashboard1.html",username=username)

# Task - /movies/add -> Add movie form (5 fields) -> Submit -> /movies-list
@app.route("/movies/add", methods=["GET"])
def add_movie_form():
    return render_template("add_movie.html")

@app.route("/movie-list.html", methods=["POST"])
def movie_form_values():
    movie_name = request.form.get("movie_name")
    poster_url = request.form.get("poster_url")
    rating = request.form.get("rating")
    summary = request.form.get("summary")
    trailer_url = request.form.get("trailer_url")
    id = str(int(max(movies, key=lambda x: int(x["id"]))["id"]) + 1)
    ans = {'id': id, 'name': movie_name, 'rating': rating,'summary': summary,'trailer':trailer_url}
    movies.append(ans)
    print("Dashboard page", ans)
    return render_template("movie-list.html",movies = movies)



# /movies --> JSON
@app.get("/movies")
def get_movies():
    return jsonify(movies)


# /movies/id
# @app.get("/movies/<id>")
# def get_specific_movies(id):
#     ans = list(filter(lambda x: x["id"] == id, movies))
#     return jsonify(ans[0])


# @app.get("/movies/<id>")
# def get_specific_movies(id):
#     filtered_movie = list(filter(lambda x: x["id"] == id, movies))
#     if len(filtered_movie) > 0:
#         return jsonify(filtered_movie[0])
#     else:
#         return "Not found", 404


# Generator expression
@app.get("/movies/<id>")
def get_specific_movies(id):
    filtered_movie = next((movie for movie in movies if movie["id"] == id), None)
    if filtered_movie is None:
        return {"message": "Movie Not found"}, 404
    return jsonify(filtered_movie)


# request.json --> new_movie
# print(movie) --> print in the console log / terminal
# 1 more than the Id
@app.post("/movies")
def add_movies():
    new_movie = request.json
    id = str(int(max(movies, key=lambda x: int(x["id"]))["id"]) + 1)
    new_movie = {**new_movie, "id": id}
    movies.append(new_movie)
    result = {"message": "added successfully", "data": new_movie}
    return jsonify(result), 201


# @app.delete("/movies/<id>")
# def delete_movie(id):
#     filtered_movie = next((movie for movie in movies if movie["id"] == id), None)
#     if filtered_movie is None:
#         return "Movie Not found", 404
#     movies = [movie for movie in movies if movie["id"] != id]
#     return jsonify(filtered_movie)


# @app.delete("/movies/<id>")
# def delete_movie(id):
#     filtered_movie = next((movie for movie in movies if movie["id"] == id), None)
#     movies.remove(filtered_movie)
#     return jsonify(filtered_movie)


@app.delete("/movies/<id>")
def delete_movie(id):
    filtered_movie = next((movie for movie in movies if movie["id"] == id), None)
    if filtered_movie is None:
        return {"message": "Movie Not found"}, 404
    movies.remove(filtered_movie)
    return jsonify(filtered_movie)


# @app.delete("/movies/<id>")
# def delete_movie(id):
#     # Permission to modify the lexical scope variable | Reassigning is not allowed
#     global movies
#     filtered_movie = next((movie for movie in movies if movie["id"] == id), None)
#     if filtered_movie is None:
#         return {"message": "Movie Not found"}, 404
#     movies = [movie for movie in movies if movie["id"] != id]
#     return jsonify(filtered_movie)


# @app.put("/movies/<id>")
# def update_movies(id):
#     movie_update = request.json
#     filtered_movie = next(
#         (ind for ind in range(len(movies)) if movies[ind]["id"] == id), None
#     )
#     if filtered_movie is None:
#         return {"message": "Movie Not found"}, 404
#     movies[filtered_movie].update(movie_update)
#     result = {"message": "updated successfully", "data": movies[filtered_movie]}
#     return jsonify(result)


@app.put("/movies/<id>")
def update_movies(id):
    movie_update = request.json
    filtered_movie = next((movie for movie in movies if movie["id"] == id), None)
    if filtered_movie is None:
        return jsonify({"message": "Movie Not found"}), 404
    filtered_movie.update(movie_update)
    result = {"message": "updated successfully", "data": filtered_movie}
    return jsonify(result)
