from flask import Blueprint, render_template

users = [
    {
        "id": "1",
        "name": "Dhara",
        "img": "https://i.pinimg.com/236x/db/b9/cb/dbb9cbe3b84da22c294f57cc7847977e.jpg",
        "pro": True,
    },
    {
        "id": "2",
        "name": "Arjun",
        "img": "https://images.unsplash.com/photo-1618641986557-1ecd230959aa?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8cHJvZmlsZXxlbnwwfHwwfHx8MA%3D%3D",
        "pro": False,
    },
    {
        "id": "3",
        "name": "John",
        "img": "https://imgv3.fotor.com/images/blog-richtext-image/10-profile-picture-ideas-to-make-you-stand-out.jpg",
        "pro": True,
    },
]

about_bp = Blueprint("about", __name__)


@about_bp.route("/")
def about():
    return render_template("about.html", users=users)


# @app.route("/about/<id>")
# def about_page_by_id(id):
#     filtered_user = [user for user in users if user["id"] == id]
#     if len(filtered_user) == 0:
#         return "<h2>404 User Not found</h2>"
#     return render_template("about.html", users=[filtered_user])


@about_bp.route("/<id>")
def about_page_by_id(id):
    filtered_user = next((user for user in users if user["id"] == id), None)
    if filtered_user is None:
        return "<h2>404 User Not found</h2>"
    return render_template("about.html", users=[filtered_user])
