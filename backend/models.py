import os
import json
from datetime import datetime
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy


database_path = os.environ.get('DATABASE_PATH') 

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    return db

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
    __tablename__ = 'movies'
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
            'release': self.release,
            'genres': self.genres
        }
    def response(self):
        return {
                'movie': self.format(),
                'id': self.id
            }
    def __repr__(self):
        return f'{self.format()}'


class Actors(db.Model):
    __tablename__ = 'actors'
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



class Roles(db.Model):
    __tablename__ = 'roles'
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
            'movie': self.movie
        }
    def response(self):
        return {
                'role': self.format(),
                'id': self.id
            }
    def __repr__(self):
        return f'{self.format()}'

'''
Wrappers

'''
class Search():
    def search_movies(searchTerm):
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
    def search_actors(searchName,searchGender,searchAge):
        """Get the entire actor list for a given combination of search terms
        Keyword arguments:
            searchName -- the String term to search in the name of the actors
            searchGender -- the String term to search in the gender of the actors
            searchAge -- the Integer value to search in the age of the actors
        """