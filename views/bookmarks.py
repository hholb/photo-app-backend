from flask import Response, request
from flask_restful import Resource
from models import Bookmark, db, Post
import json
from views import get_authorized_user_ids


class BookmarksListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
        self.auth_users = get_authorized_user_ids(self.current_user)
        self.auth_users.append(self.current_user.id)

    def get(self):
        # get all bookmarks owned by the current user
        bookmarks = Bookmark.query.filter(
            Bookmark.user_id == self.current_user.id).all()
        return Response(json.dumps([bookmark.to_dict() for bookmark in bookmarks]), mimetype="application/json", status=200)

    def post(self):
        # create a new "bookmark" based on the data posted in the body
        body = request.get_json()
        print(body)
        try:
            post_id = body.get('post_id')
            if post_id is None:
                raise ValueError
            post_id = int(post_id)
        except ValueError:
            return f"BAD REQUEST: Invalid post_id.", 400

        post = Post.query.get(body.get('post_id'))
        if post is None:
            return f"BAD REQUEST: no post with id {post_id} found.", 404
        elif post.user_id not in self.auth_users:
            return f"BAD REQUEST: Unauthorized access to post {post_id}", 404

        current_bookmarks = Bookmark.query.filter(Bookmark.user_id == self.current_user.id).all()
        bookmarked_posts = (bm.post_id for bm in current_bookmarks)
        if post_id in bookmarked_posts:
            return "BAD REQUEST: Bookmark already exists", 400
        new_bookmark = Bookmark(
            user_id=self.current_user.id, post_id=post_id)
        db.session.add(new_bookmark)
        db.session.commit()

        return Response(json.dumps(new_bookmark.to_dict()), mimetype="application/json", status=201)


class BookmarkDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user

    def delete(self, id):
        # delete "bookmark" record where "id"=id
        print(id)
        bookmark = Bookmark.query.get(id)
        if bookmark is not None:
            if bookmark.user_id != self.current_user.id:
                return "BAD REQUEST: Unable to delete bookmark.", 404
            db.session.delete(bookmark)
            db.session.commit()
            return Response(json.dumps({"text": f"Bookmark {id} deleted"}), mimetype="application/json", status=200)
        else:
            return "BAD REQUEST: Bookmark not found.", 404
        


def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint,
        '/api/bookmarks',
        '/api/bookmarks/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint,
        '/api/bookmarks/<int:id>',
        '/api/bookmarks/<int:id>',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
