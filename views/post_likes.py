from flask import Response, request
from flask_restful import Resource
from models import LikePost, db, Post
import json

from views import get_authorized_user_ids

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
        self.auth_users = get_authorized_user_ids(self.current_user)
        self.auth_users.append(self.current_user.id)
    
    def post(self):
        # create a new "like_post" based on the data posted in the body 
        body = request.get_json()
        print(body)
        try:
            post_id = body.get('post_id')
            if not post_id:
                    raise
            post_id = int(post_id)
        except ValueError:
            return "BAD REQUEST: Invalid post_id.", 400
        except:
            return "BAD REQUEST", 404
        
        post = Post.query.get(post_id)
        if post is None:
            return "BAD REQUEST: post not found", 404
        else:
            likes = (like.user_id for like in post.likes)
        if post.user_id not in self.auth_users:
            return "BAD REQEUST: unable to like post.", 404
        elif self.current_user.id in likes:
            return "BAD REQUEST: post already liked", 400
        like = LikePost(user_id=self.current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
            
        return Response(json.dumps(like.to_dict()), mimetype="application/json", status=201)

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # delete "like_post" where "id"=id
        print(id)
        like = LikePost.query.get(id)
        if like is None:
            return "BAD REQUEST: like not found", 404
        elif like.user_id != self.current_user.id:
            return "BAD REQUEST: unable to unlike post", 404
        db.session.delete(like)
        db.session.commit()
        return Response(json.dumps({"text": "like deleted"}), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/likes', 
        '/api/posts/likes/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/likes/<int:id>', 
        '/api/posts/likes/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
