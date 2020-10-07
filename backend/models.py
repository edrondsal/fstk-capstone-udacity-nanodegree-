import os
import json
from datetime import datetime
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


database_path = os.environ.get('DATABASE_PATH') 


db = SQLAlchemy()

'''flask_sqlalchemy
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app,db)
    

'''
Configuration

'''
MAX_MOVIES_PER_PAGE = 10
MAX_ACTORS_PER_PAGE = 10

'''
Models

'''

#Many to Many Relationships
movies_roles_items = db.Table('roles_in_movies',
    db.Column('movie_id', db.Integer, db.ForeignKey('Movies.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('Roles.id'), primary_key=True),
)

roles_actors_items = db.Table('actors_for_roles',
    db.Column('role_id', db.Integer, db.ForeignKey('Roles.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('Actors.id'), primary_key=True),
)

class Movies(db.Model):
    __tablename__ = 'Movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    photoUrl = db.Column(db.String(), nullable=True,default="")
    release = db.Column(db.DateTime,nullable=False)
    genres =  db.Column(db.ARRAY(db.String()),nullable=False,server_default="{}") 
    roles = db.relationship('Roles', secondary=movies_roles_items,lazy='subquery',backref=db.backref('movie', lazy=True))
    
    def __init__(name, photo, release, genres):
        self.name = name
        self.photoUrl = photo
        self.release = release
        self.genres = genres
    def insert(self):
        responseStruct = None
        try:
            db.session.add(self)
            db.session.commit()
            responseStruct = self.response()
        except:
            db.session.rollback()
        finally:
            db.session.close()
        return responseStruct
    def update(self):
        responseStruct = None
        try:
            db.session.commit()
            responseStruct = self.response()
        except:
            db.session.rollback()    
        finally:
            db.session.close()  
        return responseStruct  
    def delete(self):
        responseStruct = None
        try:        
            db.session.delete(self)
            db.session.commit()
            responseStruct = self.response()
        except:
            db.session.rollback()    
        finally:
            db.session.close()  
        return responseStruct            
    def format(self):
        return {
            'name': self.name,
            'photoUrl': self.photoUrl,
            'release': self.release.isoformat(),
            'genres': self.genres,
            'roles': [role.format() for role in self.roles]
        }
    def response(self):
        return {
                'movie': self.format(),
                'id': self.id
            }
    def __repr__(self):
        return f'{self.format()}'
    @staticmethod
    def search(searchTerm):
        """Get the entire movies list for a certain search word
        Keyword arguments:
            searchTerm -- the String term to search in the name of the movies
        """
        search = f'%{searchTerm}%'
        #query the movie with WHERE LIKE case insentive
        movies = Movies.query.filter(Movies.name.ilike(search)).all()
        if len(movies) == 0:
            return {'movies':[]}
        return { 'movies': [movie.format() for movie in movies] }
    @staticmethod
    def read(id):
        """Get the movie for an id
        Keyword arguments:
            id -- the integer id of the movie
        """
        movie = Movies.query.get(id)
        if movie is None:
            return None
        return movie.response()
    @staticmethod
    def read_all(page=0):
        """Get all movies per page
        Keyword arguments:
            page -- the integer page number
        """
        movies = Movies.query.all()
        total = len(movies)

        if page == -1:
            return { 'movies': [movie.format() for movie in movies], 'total': total, 'count': total}
        offset = (page-1)*MAX_MOVIES_PER_PAGE
        if offset > total:
            return None
        limit = min(offset + MAX_MOVIES_PER_PAGE,total-1)
        return { 'movies': [movie.format() for movie in movies][offset:limit], 'total': total, 'count':limit-offset}
    @staticmethod
    def read_artists(id):
        """Get overall artist casting for a movie
        Keyword arguments:
            id -- the integer id of the movie
        """
        movie = Movies.query.get(id)
        if movie is None:
            return None
        actors = []
        for role in movie.roles:
            for actor in role.actors:
                if actor not in actors:
                    actors.append(actor)
        return { 'actors': [actor.format() for actor in actors], 'movie': movie.format()}

class Actors(db.Model):
    __tablename__ = 'Actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    photoUrl = db.Column(db.String(), nullable=True,default="")
    gender = db.Column(db.String(),nullable=False)
    age =  db.Column(db.Integer,nullable=False)
    
    def __init__(name, photo, gender, age):
        self.name = name
        self.photoUrl = photo
        self.gender = gender
        self.age = age
    def insert(self):
        responseStruct = None
        try:
            db.session.add(self)
            db.session.commit()
            responseStruct = self.response()
        except:
            db.session.rollback()
        finally:
            db.session.close()
        return responseStruct
    def update(self):
        responseStruct = None
        try:
            db.session.commit()
            responseStruct = self.response()
        except:
            db.session.rollback()    
        finally:
            db.session.close()  
        return responseStruct  
    def delete(self):
        responseStruct = None
        try:        
            db.session.delete(self)
            db.session.commit()
            responseStruct = self.response()
        except:
            db.session.rollback()    
        finally:
            db.session.close()  
        return responseStruct            
    def format(self):
        return {
            'name': self.name,
            'photoUrl': self.photoUrl,
            'gender': self.gender,
            'age': self.age
        }
    def response(self):
        return {
                'actor': self.format(),
                'id': self.id
            }
    def __repr__(self):
        return f'{self.format()}'
    @staticmethod
    def search(searchName=None,searchGender=None,searchAge=None):
        """Get the entire actor list for a given combination of search terms
        Keyword arguments:
            searchName -- the String term to search in the name of the actors
            searchGender -- the String term to search in the gender of the actors
            searchAge -- the Integer value to search in the age of the actors
        """
        if searchName == None and searchGender == None and searchAge == None:
            return {'actors':[]}
        query_search = Actors.query
        if searchName != None:
            search = f'%{searchName}%'
            query_search = query_search.filter(Actors.name.ilike(search))
        if searchGender != None:
            query_search = query_search.filter(Actors.gender == searchGender)
        if searchAge != None:
            query_search = query_search.filter(Actors.age == searchAge)
        actors = query_search.all()
        if len(actors) == 0:
            return {'actors':[]} 
        return {'actors': [actor.format() for actor in actors]}
    @staticmethod
    def read(id):
        """Get the actor for an id
        Keyword arguments:
            id -- the integer id to search
        """
        item = Actors.query.get(id)
        if item is None:
            return None
        return item.response()
    @staticmethod
    def read_all(page=0):
        """Get all actors per page
        Keyword arguments:
            page -- the integer page number
        """
        items = Actors.query.all()
        total = len(items)

        if page == -1:
            return { 'actors': [item.format() for item in items], 'total': total, 'count': total}
        offset = (page-1)*MAX_ACTORS_PER_PAGE
        if offset > total:
            return None
        limit = min(offset + MAX_ACTORS_PER_PAGE,total-1)
        return { 'actors': [item.format() for item in items][offset:limit], 'total': total, 'count':limit-offset}

class Roles(db.Model):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    types = db.Column(db.String(), nullable=False)
    actors = db.relationship('Actors', secondary=roles_actors_items,lazy='subquery',backref=db.backref('roles', lazy=True))
    movie = db.Column(db.Integer, db.ForeignKey('Movies.id'),nullable=False)

    def __init__(name, types, movie_id):
        self.name = name
        self.types = types
        self.movie = movie_id
    def insert(self):
        responseStruct = None
        try:
            db.session.add(self)
            db.session.commit()
            responseStruct = self.response()
        except:
            db.session.rollback()
        finally:
            db.session.close()
        return responseStruct
    def update(self):
        responseStruct = None
        try:
            db.session.commit()
            responseStruct = self.response()
        except:
            db.session.rollback()    
        finally:
            db.session.close()  
        return responseStruct  
    def delete(self):
        responseStruct = None
        try:        
            db.session.delete(self)
            db.session.commit()
            responseStruct = self.response()
        except:
            db.session.rollback()    
        finally:
            db.session.close()  
        return responseStruct            
    def format(self):
        return {
            'name': self.name,
            'types': self.types,
            'movie': self.movie,
            'actors': [actor.format() for actor in self.actors]
        }
    def response(self):
        return {
                'role': self.format(),
                'id': self.id
            }
    def __repr__(self):
        return f'{self.format()}'



