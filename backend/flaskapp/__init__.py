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
        """Retrieve the movies for the page requested in the query
        Keyword arguments:
        """
        page = request.args.get('page', -1, type=int)
        responseStruct = Movies.read_all(page)
        if responseStruct is None:
            abort(404)
        return Response.success_response(responseStruct), 200
    
    @app.route('/movies/search', methods=['POST'])
    def search_movies():
        body = request.get_json()
        searchTerm = body.get('searchTerm',None)
        if searchTerm is None:
            abort(422)
        responseStruct = Movies.search(searchTerm)
        return Response.success_response(responseStruct), 200

    @app.route('/movies/<int:id>/actors', methods=['GET'])
    def read_movie_actors(id):
        responseStruct = Movies.read_artists(id)
        if responseStruct is None:
            abort(404)
        return Response.success_response(responseStruct)

    # Start of CRUD methods endpoints
    @app.route('/movies', methods=['POST'])
    def create_movie():
        body = request.get_json()
        name = body.get('name',None)
        genres = body.get('genres',None)
        timestamp = body.get('timestamp',None)
        photoUrl = body.get('photourl',"")
        if name is None or genres is None or timestamp is None:
            abort(422)
        release = datetime.fromtimestamp(timestamp)
        movie = Movies(name=name,photo=photoUrl,release=release,genres=genres)
        responseStruct = movie.insert()
        if responseStruct is None:
            abort(500)
        return Response.success_response(responseStruct), 201

    @app.route('/movies/<int:id>', methods=['GET'])
    def read_movie(id):
        response_data = Movies.read(id)
        if response_data is None:
            abort(404)
        return Response.success_response(response_data) , 200

    @app.route('/movies/<int:id>', methods=['PATCH'])
    def update_movie(id):
        movie = Movies.get(id)
        if movie is None:
            abort(404)
        body = request.get_json()
        name = body.get('name',None)
        genres = body.get('genres',None)
        timestamp = body.get('timestamp',None)
        photoUrl = body.get('photourl',None)
        if name is None and genres is None and timestamp is None and photoUrl is None:
            abort(422)   
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
            abort(500)
        return Response.success_response(responseStruct), 200
                   
    @app.route('/movies/<int:id>', methods=['DELETE'])
    def delete_movie(id):   
        movie = Movies.get(id)
        if movie is None:
            abort(404)
        responseStruct = movie.delete()
        if responseStruct is None:
            abort(500)
        return Response.success_response(responseStruct), 200
    
    #  Actors Endpoints
    #  ----------------------------------------------------------------    
    # start list methods endpoints 
    @app.route('/actors', methods=['GET'])
    def get_actors():
        """Retrieve the actors for the page requested in the query
        Keyword arguments:
        """
        page = request.args.get('page', -1, type=int)
        responseStruct = Actors.read_all(page)
        if responseStruct is None:
            abort(404)
        return Response.success_response(responseStruct), 200        
    
    @app.route('/actors/search', methods=['POST'])
    def search_actors():
        body = request.get_json()
        searchName = body.get('searchName',None)
        searchGender = body.get('searchGender',None)
        searchName = body.get('searchAge',None)
        if searchName is None and searchGender is None and searchName is None:
            abort(422)
        responseStruct = Actors.search(searchName=searchName,searchGender=searchGender,searchAge=searchAge)
        return Response.success_response(responseStruct), 200        

    # Start of CRUD methods endpoints
    @app.route('/actors', methods=['POST'])
    def create_actor():
        body = request.get_json()
        name = body.get('name',None)
        gender = body.get('gender',None)
        age = body.get('age',None)
        photoUrl = body.get('photourl',"")
        if name is None or gender is None or age is None:
            abort(422)
        actor = Actors(name=name,photo=photoUrl,gender=gender,age=age)
        responseStruct = actor.insert()
        if responseStruct is None:
            abort(500)
        return Response.success_response(responseStruct), 201

    @app.route('/actors/<int:id>', methods=['GET'])
    def read_actor(id):
        response_data = Actors.read(id)
        if response_data is None:
            abort(404)
        return Response.success_response(response_data) , 200

    @app.route('/actors/<int:id>', methods=['PATCH'])
    def update_actor(id):  
        actor = Actors.get(id)
        if actor is None:
            abort(404)
        body = request.get_json()
        name = body.get('name',None)
        gender = body.get('gender',None)
        age = body.get('age',None)
        photoUrl = body.get('photourl',None)
        if name is None and gender is None and age is None and photoUrl is None:
            abort(422)   
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
            abort(500)
        return Response.success_response(responseStruct), 200
    
    @app.route('/actors/<int:id>', methods=['DELETE'])
    def delete_actor(id): 
        actor = Actors.get(id)
        if actor is None:
            abort(404)
        responseStruct = actor.delete()
        if responseStruct is None:
            abort(500)
        return Response.success_response(responseStruct), 200

    #  Roles Endpoints
    #  ----------------------------------------------------------------     
    # Start of CRUD methods endpoints
    @app.route('/roles', methods=['POST'])
    def create_role():
        body = request.get_json()
        name = body.get('name',None)
        roletype = body.get('type',None)
        movie_id = body.get('movie',None)
        if name is None or roletype is None or movie_id is None:
            abort(422)
        movie = Movies.get(movie_id)
        if movie is None:
            abort(422)
        role = Roles(name=name,types=roletype,movie_id=movie_id)
        movie.roles.append(role)

        responseStruct = role.insert()
        temp = movie.update()
        if responseStruct is None or temp is None:
            abort(500)
        return Response.success_response(responseStruct), 201
        
    @app.route('/roles/<int:id>', methods=['PATCH'])
    def update_role(id):
        body = request.get_json()
        name = body.get('name',None)
        roletype = body.get('type',None)
        actor_id = body.get('actor',None)  
        if name is None and roletype is None and actor_id is None:
            abort(422)
        role = Roles.get(id)
        if role is None:
            abort(404)
        if name is not None:
            role.name = name
        if roletype is not None:
            role.types = roletype
        if actor_id is not None:
            actor = Actors.get(actor_id)
            if actor is None:
                abort(422)
            role.actors.append(actor)
        responseStruct = role.update()
        if responseStruct is None:
            abort(500)
        return Response.success_response(responseStruct), 200    

    #  Error Handlers
    #  ----------------------------------------------------------------
    return app