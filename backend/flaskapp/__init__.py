import os
import random
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Roles, Actors
from responses import Response, AppError
from authorization import requires_auth
from datetime import datetime



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
    @requires_auth('get:movies')
    def get_movies():
        """Retrieve the movies for the page requested in the query
        Keyword arguments:
        """
        page = request.args.get('page', -1, type=int)
        responseStruct = Movies.read_all(page)
        if responseStruct is None:
            raise AppError(title='Wrong Pagination', detail='page not found', status_code=404)
        return Response.success_response(responseStruct), 200
    
    @app.route('/movies/search', methods=['POST'])
    @requires_auth('get:movies')
    def search_movies():
        body = request.get_json()
        searchTerm = body.get('searchTerm',None)
        if searchTerm is None:
            raise AppError(title='Wrong Search Request', detail='searchTerm not found in body of the request', status_code=404)
        responseStruct = Movies.search(searchTerm)
        return Response.success_response(responseStruct), 200

    @app.route('/movies/<int:id>/actors', methods=['GET'])
    @requires_auth('get:actors')
    def read_movie_actors(id):
        responseStruct = Movies.read_artists(id)
        if responseStruct is None:
            raise AppError(title='Wrong Id', detail='Id request not found', status_code=404)
        return Response.success_response(responseStruct)

    # Start of CRUD methods endpoints
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie():
        body = request.get_json()
        name = body.get('name',None)
        genres = body.get('genres',None)
        timestamp = body.get('timestamp',None)
        photoUrl = body.get('photourl',"")
        if name is None or genres is None or timestamp is None:
            raise AppError(title='Wrong Create Request', detail='Name, Genres or Timestamp is missing', status_code=422)
        release = datetime.fromtimestamp(timestamp)
        movie = Movies(name=name,photo=photoUrl,release=release,genres=genres)
        responseStruct = movie.insert()
        if responseStruct is None:
            raise AppError(title='Internal Server Error', detail='Internal problem while processing the request', status_code=500)
        return Response.success_response(responseStruct), 201

    @app.route('/movies/<int:id>', methods=['GET'])
    @requires_auth('get:movies')
    def read_movie(id):
        response_data = Movies.read(id)
        if response_data is None:
            raise AppError(title='Wrong Id', detail='Id request not found', status_code=404)
        return Response.success_response(response_data) , 200

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(id):
        movie = Movies.get(id)
        if movie is None:
            raise AppError(title='Wrong Id', detail='Id request not found', status_code=404)
        body = request.get_json()
        name = body.get('name',None)
        genres = body.get('genres',None)
        timestamp = body.get('timestamp',None)
        photoUrl = body.get('photourl',None)
        if name is None and genres is None and timestamp is None and photoUrl is None:
            raise AppError(title='Wrong Update Request', detail='Name, Genres, Timestamp and photoUrl are missing', status_code=422)   
        if name is not None:
            movie.name = name
        if genres is not None:
            movie.genres = genres
        if timestamp is not None:
            release = datetime.fromtimestamp(timestamp)
            movie.release = release
        if photoUrl is not None:
            movie.photoUrl = photoUrl
        responseStruct = movie.update()
        if responseStruct is None:
            raise AppError(title='Internal Server Error', detail='Internal problem while processing the request', status_code=500)
        return Response.success_response(responseStruct), 200
                   
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(id):   
        movie = Movies.get(id)
        if movie is None:
            raise AppError(title='Wrong Id', detail='Id request not found', status_code=404)
        responseStruct = movie.delete()
        if responseStruct is None:
            raise AppError(title='Internal Server Error', detail='Internal problem while processing the request', status_code=500)
        return Response.success_response(responseStruct), 200
    
    #  Actors Endpoints
    #  ----------------------------------------------------------------    
    # start list methods endpoints 
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        """Retrieve the actors for the page requested in the query
        Keyword arguments:
        """
        page = request.args.get('page', -1, type=int)
        responseStruct = Actors.read_all(page)
        if responseStruct is None:
            raise AppError(title='Wrong Pagination', detail='Page requested does not exist', status_code=404)
        return Response.success_response(responseStruct), 200        
    
    @app.route('/actors/search', methods=['POST'])
    @requires_auth('get:actors')
    def search_actors():
        body = request.get_json()
        searchName = body.get('searchName',None)
        searchGender = body.get('searchGender',None)
        searchAge = body.get('searchAge',None)
        if searchName is None and searchGender is None and searchAge is None:
            raise AppError(title='Wrong Search Request', detail='all search types are missing', status_code=422)
        responseStruct = Actors.search(searchName=searchName,searchGender=searchGender,searchAge=searchAge)
        return Response.success_response(responseStruct), 200        

    # Start of CRUD methods endpoints
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor():
        body = request.get_json()
        name = body.get('name',None)
        gender = body.get('gender',None)
        age = body.get('age',None)
        photoUrl = body.get('photourl',"")
        if name is None or gender is None or age is None:
            raise AppError(title='Wrong Create Request', detail='Name, Gender or Age is missing', status_code=422)
        actor = Actors(name=name,photo=photoUrl,gender=gender,age=age)
        responseStruct = actor.insert()
        if responseStruct is None:
            raise AppError(title='Internal Server Error', detail='Internal problem while processing the request', status_code=500)
        return Response.success_response(responseStruct), 201

    @app.route('/actors/<int:id>', methods=['GET'])
    @requires_auth('get:actors')
    def read_actor(id):
        response_data = Actors.read(id)
        if response_data is None:
            raise AppError(title='Wrong Id', detail='Id request not found', status_code=404)
        return Response.success_response(response_data) , 200

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(id):  
        actor = Actors.get(id)
        if actor is None:
            raise AppError(title='Wrong Id', detail='Id request not found', status_code=404)
        body = request.get_json()
        name = body.get('name',None)
        gender = body.get('gender',None)
        age = body.get('age',None)
        photoUrl = body.get('photourl',None)
        if name is None and gender is None and age is None and photoUrl is None:
            raise AppError(title='Wrong Update Request', detail='Name, Gender, Age and photoUrl are missing', status_code=422)  
        if name is not None:
            actor.name = name
        if gender is not None:
           actor.gender = gender
        if age is not None:
            actor.age = age
        if photoUrl is not None:
            actor.photoUrl = photoUrl
        responseStruct = actor.update()
        if responseStruct is None:
            raise AppError(title='Internal Server Error', detail='Internal problem while processing the request', status_code=500)
        return Response.success_response(responseStruct), 200
    
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(id): 
        actor = Actors.get(id)
        if actor is None:
            raise AppError(title='Wrong Id', detail='Id request not found', status_code=404)
        responseStruct = actor.delete()
        if responseStruct is None:
            raise AppError(title='Internal Server Error', detail='Internal problem while processing the request', status_code=500)
        return Response.success_response(responseStruct), 200

    #  Roles Endpoints
    #  ----------------------------------------------------------------     
    # Start of CRUD methods endpoints
    @app.route('/roles', methods=['POST'])
    @requires_auth('post:roles')
    def create_role():
        body = request.get_json()
        name = body.get('name',None)
        roletype = body.get('type',None)
        movie_id = body.get('movie',None)
        if name is None or roletype is None or movie_id is None:
            raise AppError(title='Wrong Create Request', detail='Name, Tye of Role or Movie ID is missing', status_code=422)
        movie = Movies.get(movie_id)
        if movie is None:
            raise AppError(title='Wrong Create Request', detail='Movie with requested ID does not exist', status_code=422)
        role = Roles(name=name,types=roletype,movie_id=movie_id)
        movie.roles.append(role)

        responseStruct = role.insert()
        
        if responseStruct is None:
            raise AppError(title='Internal Server Error', detail='Internal problem while processing the request', status_code=500)
        return Response.success_response(responseStruct), 201
        
    @app.route('/roles/<int:id>', methods=['PATCH'])
    @requires_auth('patch:roles')
    def update_role(id):
        body = request.get_json()
        name = body.get('name',None)
        roletype = body.get('type',None)
        actor_id = body.get('actor',None)  
        if name is None and roletype is None and actor_id is None:
            raise AppError(title='Wrong Patch Request', detail='Name, Type of Role, and Actor ID are missing', status_code=422)
        role = Roles.get(id)
        if role is None:
            raise AppError(title='Wrong Id', detail='Id request not found', status_code=404)
        if name is not None:
            role.name = name
        if roletype is not None:
            role.types = roletype
        if actor_id is not None:
            actor = Actors.get(actor_id)
            if actor is None:
                raise AppError(title='Wrong Patch Request', detail='Actor with requested ID does not exist', status_code=422)
            role.actors.append(actor)
        responseStruct = role.update()
        if responseStruct is None:
             raise AppError(title='Internal Server Error', detail='Internal problem while processing the request', status_code=500)
        return Response.success_response(responseStruct), 200    

    #  Error Handlers
    #  ----------------------------------------------------------------
    @app.errorhandler(AppError)
    def response_error(e):
        return Response.error_response(e), e.status_code
    return app