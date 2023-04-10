from flask import Response, request
from flask_restful import Resource
from models import Post, db, Following
from views import get_authorized_user_ids

import json

def get_path():
    return request.host_url + 'api/posts/'

class PostListEndpoint(Resource):

    
    def __init__(self, current_user):
        self.current_user = current_user
        self.auth_users = get_authorized_user_ids(self.current_user)
        self.auth_users.append(self.current_user.id)

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

        posts = Post.query.filter(Post.user_id.in_(self.auth_users)).limit(num_posts).all()
        return Response(json.dumps([post.to_dict() for post in posts]), mimetype="application/json", status=200)

    def post(self):
        # create a new post based on the data posted in the body 
        body = request.get_json()
        print(body)
        return Response(json.dumps({}), mimetype="application/json", status=201)
        
class PostDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
        self.auth_users = get_authorized_user_ids(self.current_user)
        self.auth_users.append(self.current_user.id)
        

    def patch(self, id):
        # update post based on the data posted in the body 
        body = request.get_json()
        print(body)       
        return Response(json.dumps({}), mimetype="application/json", status=200)


    def delete(self, id):
        # delete post where "id"=id
        return Response(json.dumps({}), mimetype="application/json", status=200)


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
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        PostDetailEndpoint, 
        '/api/posts/<int:id>', '/api/posts/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )