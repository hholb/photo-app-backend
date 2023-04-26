from flask import Response, request
import flask_jwt_extended
from flask_restful import Resource
from models import Post, Bookmark, db, Following
from views import get_authorized_user_ids

import json


def get_path():
    return request.host_url + 'api/posts/'


class PostListEndpoint(Resource):

    @flask_jwt_extended.jwt_required()
    def __init__(self, current_user):
        self.current_user = current_user
        self.auth_users = get_authorized_user_ids(self.current_user)
        self.auth_users.append(self.current_user.id)

    @flask_jwt_extended.jwt_required()
    def get(self):
        # get posts created by one of these users:
        if request.args.get('limit') is not None:
            try:
                num_posts = int(request.args.get('limit'))
                if num_posts > 50:
                    raise ValueError
            except ValueError:
                return "BAD REQUEST: limit must be an int less than 50", 400
        else:
            num_posts = 20

        posts = Post.query.filter(Post.user_id.in_(
            self.auth_users)).limit(num_posts).all()
        return Response(json.dumps([post.to_dict() for post in posts]), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    def post(self):
        # create a new post based on the data posted in the body
        body = request.get_json()
        print(body)
        if not body.get('image_url'):
            return "BAD REQUEST: image_url required", 400
        else:
            post = Post(
                image_url=body.get('image_url'),
                user_id=self.current_user.id,
                caption=body.get('caption'),
                alt_text=body.get('alt_text')
            )
            db.session.add(post)
            db.session.commit()

            return Response(json.dumps(post.to_dict()), mimetype="application/json", status=201)


class PostDetailEndpoint(Resource):

    @flask_jwt_extended.jwt_required()
    def __init__(self, current_user):
        self.current_user = current_user
        self.auth_users = get_authorized_user_ids(self.current_user)
        self.auth_users.append(self.current_user.id)

    @flask_jwt_extended.jwt_required()
    def patch(self, id):
        # update post based on the data posted in the body
        post = Post.query.get(id)
        body = request.get_json()
        print(body, post)
        if post is not None:
            if post.user_id != self.current_user.id:
                return f"Unable to access post with id:{id}", 404
            keys = ('image_url', 'caption', 'alt_text')
            for key in keys:
                if body.get(key) is not None:
                    match key:
                        case "image_url":
                            post.image_url = body.get('image_url')
                        case "caption":
                            post.caption = body.get('caption')
                        case "alt_text":
                            post.alt_text = body.get('alt_text')
            db.session.add(post)
            db.session.commit()
        else:
            return f"BAD REQUEST: No post with id {id} found.", 404
        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        # delete post where "id"=id
        try:
            post_id = int(id)
        except ValueError:
            return f"BAD REQUEST: Expecting post id as int", 404
        post = Post.query.get(post_id)
        if post is not None:
            if post.user_id != self.current_user.id:
                return f"Unable to access post with id:{id}", 404
            bookmarks = Bookmark.query.filter(Bookmark.post_id == post_id).all()
            for bookmark in bookmarks:
                db.session.delete(bookmark)
            db.session.delete(post)
            db.session.commit()
        else:
            return f"BAD REQUEST: No post with id {id} found.", 404
        return Response(json.dumps({"text": f"Post with id {id} deleted."}), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    def get(self, id):
        # get the post based on the id
        post = Post.query.get(id)
        if post is not None:
            if post.user_id not in self.auth_users:
                return f"Unable to access post with id:{id}", 404
            return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)
        else:
            return f"No posts with id:{id} found.", 404


def initialize_routes(api):
    api.add_resource(
        PostListEndpoint,
        '/api/posts', '/api/posts/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
    api.add_resource(
        PostDetailEndpoint,
        '/api/posts/<int:id>', '/api/posts/<int:id>/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
