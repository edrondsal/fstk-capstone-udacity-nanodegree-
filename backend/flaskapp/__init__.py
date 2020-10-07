import os
import random
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Roles, Actors
from responses import Response



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    # CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response


    #  Movies Endpoints
    #  ----------------------------------------------------------------  
    # start list methods endpoints 
    @app.route('/movies', methods=['GET'])
    def get_movies():
    
    @app.route('/movies/search', methods=['POST'])
    def search_movies():

    @app.route('/movies/<int:id>/actors', methods=['GET'])
    def read_movie_actors():

    # Start of CRUD methods endpoints
    @app.route('/movies', methods=['POST'])
    def create_movie():

    @app.route('/movies/<int:id>', methods=['GET'])
    def read_movie():

    @app.route('/movies/<int:id>', methods=['PATCH'])
    def update_movie():  

    @app.route('/movies/<int:id>', methods=['DELETE'])
    def delete_movie():   

    #  Actors Endpoints
    #  ----------------------------------------------------------------    


    #  Roles Endpoints
    #  ----------------------------------------------------------------     

    #  Error Handlers
    #  ----------------------------------------------------------------
    return app