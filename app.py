from flask import Flask, request, redirect, url_for
from flask_restful import Api, Resource
from models import db, Post

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return redirect(url_for("posts"))

class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return [post.to_dict() for post in posts], 200

    def post(self):
        data = request.get_json()

        if not data or not data.get("title") or not data.get("content"):
            return {"error": "Title and Content are required"}, 400

        new_post = Post(
            title=data["title"],
            content=data["content"],
            author=data.get("author", "Anonymous")
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post.to_dict(), 201

class PostResource(Resource):
    def get(self, id):
        post = Post.query.get_or_404(id)
        return post.to_dict(), 200

    def put(self, id):
        post = Post.query.get_or_404(id)
        data = request.get_json()

        if "title" in data:
            post.title = data["title"]
        if "content" in data:
            post.content = data["content"]
        if "author" in data:
            post.author = data["author"]

        db.session.commit()
        return post.to_dict(), 200

    def delete(self, id):
        post = Post.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted"}, 200

api.add_resource(PostListResource, "/posts", endpoint="posts")
api.add_resource(PostResource, "/posts/<int:id>", endpoint="post")

if __name__ == "__main__":
    app.run(debug=False)

