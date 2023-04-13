from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import json

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # return all of the "following" records that the current user is following
        following = Following.query.filter(Following.user_id == self.current_user.id).all()
        return Response(json.dumps([follow.to_dict_following() for follow in following]), mimetype="application/json", status=200)

    def post(self):
        # create a new "following" record based on the data posted in the body 
        body = request.get_json()
        print(body)
        user_id = body.get('user_id')
        try:
            if not user_id:
                raise
            user_id = int(user_id)
        except:
            return "BAD REQUEST", 400
        user = User.query.get(user_id)
        if user is None:
            return "BAD REQUEST: unknown user_id", 404
        following = Following.query.filter(Following.user_id == self.current_user.id).all()
        following_ids = (follow.following_id for follow in following)
        if user_id in following_ids:
            return "BAD REQUEST: already following user", 400
        follow = Following(user_id=self.current_user.id, following_id=user_id)
        db.session.add(follow)
        db.session.commit()
        return Response(json.dumps(follow.to_dict_following()), mimetype="application/json", status=201)

class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # delete "following" record where "id"=id
        print(id)
        follow = Following.query.get(id)
        if follow is None:
            return "BAD REQUEST: follow not found", 404
        if follow.user_id != self.current_user.id:
            return "BAD REQUEST: unauthorized", 404
        db.session.delete(follow)
        db.session.commit()
        return Response(json.dumps({"text": "Removed Following"}), mimetype="application/json", status=200)




def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<int:id>', 
        '/api/following/<int:id>/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
