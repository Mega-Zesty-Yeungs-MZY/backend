from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource 
from datetime import datetime

from model.tests import Rankings

ranking_api = Blueprint('ranking_api', __name__,
                   url_prefix='/api/rankings')


api = Api(ranking_api)

class RankingsAPI:        
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            
            score = body.get('score')
            if score is None or len(score) < 2:
                return {'message': f'score is missing, or is less than 2 characters'}, 210
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 210

            uo = Rankings(score=score, 
                      name=name)
            
            rank = uo.create()
   
            if rank:
                return jsonify(rank.read())
            return {'message': f'Processed {score}, either a format error or User ID is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            scores = Rankings.query.all()  
            json_ready = [score.read() for score in scores]  
            return jsonify(json_ready)  

    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')