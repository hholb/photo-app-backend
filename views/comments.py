from flask import Response, request
import flask_jwt_extended
from flask_restful import Resource
import json
from models import db, Comment, Post
from views import get_authorized_user_ids

class CommentListEndpoint(Resource):

    @flask_jwt_extended.jwt_required()
    def __init__(self, current_user):
        self.current_user = current_user
        self.auth_users = get_authorized_user_ids(self.current_user)
        self.auth_users.append(self.current_user.id)
    

    @flask_jwt_extended.jwt_required()
    def post(self):
        # create a new "Comment" based on the data posted in the body 
        body = request.get_json()
        if body.get('post_id') is None or body.get('text') is None:
            return "BAD REQUEST: post_id and text required.", 400
        try:
            post_id = int(body.get('post_id'))
            post = Post.query.get(post_id)
            if post is None or post.user_id not in self.auth_users:
                raise
        except ValueError:
            return f"BAD REQUEST: Unable to access post with id {body.get('post_id')}", 400
        except:
            return f"BAD REQUEST: Unable to access post with id {body.get('post_id')}", 404
        comment = Comment(text=body.get('text'), user_id=self.current_user.id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        print(body)
        return Response(json.dumps(comment.to_dict()), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    @flask_jwt_extended.jwt_required()
    def __init__(self, current_user):
        self.current_user = current_user
  
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        # delete "Comment" record where "id"=id
        print(id)
        comment = Comment.query.get(id)
        if comment is None:
            return f"BAD REQUST: Comment with id {id} not found.", 404
        if comment.user_id != self.current_user.id:
            return f"BAD REQUEST: Unauthorized access to comment with id {id}", 404
        db.session.delete(comment)
        db.session.commit()
        return Response(json.dumps({"text": f"Comment {id} deleted"}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<int:id>', 
        '/api/comments/<int:id>/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
