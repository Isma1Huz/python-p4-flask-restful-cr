#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Index(Resource):
    def get(self):
        respons_dict = {
            "index": "Welcome to the Newsletter RESTful API",
        }

        response = make_response(
            jsonify(respons_dict),
            200
        )

        return response
    
api.add_resource(Index, '/')



class NewsLetters(Resource):
    def get(self):

        response_dict =  [newsletter.to_dict() for newsletter in Newsletter.query.all()]

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response
    
    def post(self):
        new_letter = Newsletter(
            title = request.json['title'],
            body = request.json['body'],
        )

        db.session.add(new_letter)
        db.session.commit()

        response_dict = new_letter.to_dict() 

        response = make_response(
            jsonify(response_dict),
            201
        )

        return response

api.add_resource(NewsLetters, '/newsletters')

class NewsLetterById(Resource):
    def get(self, id):
        newsletter = Newsletter.query.filter_by(id=id).first()
        
        if newsletter is None:
            # Handle the case when the newsletter with the given ID is not found
            response_dict = {"error": "Newsletter not found"}
            status_code = 404
        else:
            # Convert the newsletter object to a dictionary
            response_dict = newsletter.to_dict()
            status_code = 200

        # Create a response object with JSON data and status code
        response = make_response(
            jsonify(response_dict),
            status_code
        )

        return response

api.add_resource(NewsLetterById, '/newsletters/<int:id>')


        






if __name__ == '__main__':
    app.run(port=5555, debug=True)
