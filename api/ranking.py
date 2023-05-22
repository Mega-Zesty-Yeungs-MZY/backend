from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource 
from datetime import datetime

from model.rankings import Charges

charge_api = Blueprint('charge_api', __name__,
                   url_prefix='/api/rankings')


api = Api(charge_api)

class ChargesAPI:        
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            
            chargetime = body.get('chargetime')
            if chargetime is None or len(chargetime) < 2:
                return {'message': f'chargetime is missing, or is less than 2 characters'}, 210
            car = body.get('car')
            if car is None or len(car) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 210

            uo = Charges(chargetime=chargetime, 
                      car=car)
            
            charge = uo.create()
   
            if charge:
                return jsonify(charge.read())
            return {'message': f'Processed {chargetime}, either a format error or User ID is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            charges = Charges.query.all()  
            json_ready = [charge.read() for charge in charges]  
            return jsonify(json_ready)  

    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')