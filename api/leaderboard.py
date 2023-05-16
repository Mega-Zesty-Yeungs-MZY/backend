from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource 
from datetime import datetime

from model.leaderboards import Leaderboards

leaderboard_api = Blueprint('leaderboard_api', __name__,
                   url_prefix='/api/leaderboards')


api = Api(leaderboard_api)

class LeaderboardsAPI:        
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            
            time = body.get('time')
            if time is None or len(time) < 2:
                return {'message': f'time is missing, or is less than 2 characters'}, 210
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 210

            uo = Leaderboards(time=time, 
                      name=name)
            
            entry = uo.create()
   
            if entry:
                return jsonify(entry.read())
            return {'message': f'Processed {time}, either a format error or User ID is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            entrys = Leaderboards.query.all()  
            json_ready = [entry.read() for entry in entries]  
            return jsonify(json_ready)  

    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')