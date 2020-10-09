import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import logging
import sys
from flaskapp import create_app
from models import setup_db, Movies, Roles, Actors


class CastingAgencyUnitTest(unittest.TestCase):
    """This class represents the unit test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency_test"
        self.database_path = "postgresql://{}/{}".format('udacity:udacity@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Tests for API Endpoints
    """
    def test_get_movies_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_movies_pass")
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
    def test_get_movies_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_movies_fails")
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],404) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance'])            
    def test_get_movies_pagination_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_movies_pagination_pass")
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
    def test_get_movies_pagination_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_movies_pagination_fail")
        res = self.client().get('/movies?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],404) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance'])   
    def test_get_movies_actors_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_movies_actors_pass")
        res = self.client().get('/movies/1/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
    def test_get_movies_actors_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_movies_actors_fails")
        res = self.client().get('/movies/1/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],404) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance'])  
    def test_get_actors_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_actors_pass")
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
    def test_get_actors_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_actors_fails")
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],404) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance'])            
    def test_get_actors_pagination_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_actors_pagination_pass")
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
    def test_get_actors_pagination_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_actors_pagination_pass")
        res = self.client().get('/actors?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],404) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance'])        

    def test_search_movies_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_search_movies")
        res = self.client().post('/movies/search', json={'searchTerm': 'The'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
    def test_search_movies_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_search_movies")
        res = self.client().post('/movies/search', json={'searchTitle': 'The'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],404) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance'])  
    def test_search_actors_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_search_actors_pass")
        res = self.client().post('/actors/search', json={'searchName': 'M'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
    def test_search_actors_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_search_actors_fail")
        res = self.client().post('/actors/search', json={'searchName': 'M'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],404) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance']) 

    def test_create_movie_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_create_movies_pass")
        res = self.client().post('/movies', json={'name': 'New Movie','timestamp': 1523443804, 'genres': ['Comedy','Romantic']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
    def test_create_movie_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_create_movie_fail")
        res = self.client().post('/movies', json={'name': 'New Movie'})
        data = json.loads(res.data)    
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],422) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance'])   
    def test_create_actor_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_create_actor_pass")
        res = self.client().post('/actors', json={'name': 'New Actor','gender': 'Male', 'age': 26})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
    def test_create_actor_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_create_actor_fail")
        res = self.client().post('/actors', json={'name': 'New Actor'})
        data = json.loads(res.data)    
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],422) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance']) 
    def test_create_role_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_create_role_pass")
        res = self.client().post('/roles', json={'name': 'New Role','type': 'Lead Actor', 'movie': 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
    def test_create_role_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_create_role_fail")
        res = self.client().post('/roles', json={'name': 'New Role'})
        data = json.loads(res.data)    
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],422) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance']) 

    def test_read_movie_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_read_movies_pass")
        res = self.client().get('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
    def test_read_movie_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_read_movies_pass")
        res = self.client().get('/movies/1000')
        data = json.loads(res.data) 
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],404) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance'])   
    def test_read_actor_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_read_actors_pass")
        res = self.client().get('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
    def test_read_actor_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_read_actors_fail")
        res = self.client().get('/actors/1000')
        data = json.loads(res.data) 
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],404) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance']) 

    def test_update_movie_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_update_movies_pass")
        res = self.client().patch('/movies/1', json={'name': 'The ring'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
    def test_update_movie_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_update_movies_fail")
        res = self.client().patch('/movies/1', json={'wrongname': 'Witched'})
        data = json.loads(res.data)   
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],422) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance'])   
    def test_update_actor_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_update_actor_pass")
        res = self.client().patch('/actors/1', json={'name': 'Young Actor'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
    def test_update_actor_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_update_actor_fail")
        res = self.client().patch('/actors/1', json={'wrongname': 'New Actor'})
        data = json.loads(res.data)    
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],422) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance']) 
    def test_update_role_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_update_role_pass")
        res = self.client().patch('/roles/1', json={'name': 'The Master'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
    def test_update_role_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_update_role_fail")
        res = self.client().patch('/roles/1', json={'wrongname': 'New Role'})
        data = json.loads(res.data)    
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],422) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance'])
    
    def test_delete_movie_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_delete_movie_pass")
        movies = Movies.query.all()
        mid = movies[-1].id

        res = self.client().delete(f'/movies/{mid}')
        data = json.loads(res.data)

        movie = Movies.query.get(mid)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
        self.assertEqual(movie,None)
    def test_delete_movie_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_delete_movie_fail")
        res = self.client().delete('/movies/200')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],404) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance'])
    def test_delete_actor_pass(self):
        log = logging.getLogger("TestLog")
        log.debug("test_delete_actor_pass")
        actors = Actors.query.all()
        mid = actors[-1].id

        res = self.client().delete(f'/actors/{mid}')
        data = json.loads(res.data)

        actor = Actors.query.get(mid)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['data'])
        self.assertEqual(actor,None)
    def test_delete_movie_fail(self):
        log = logging.getLogger("TestLog")
        log.debug("test_delete_actor_fail")
        res = self.client().delete('/actors/200')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status'],404) 
        self.assertTrue(data['type'])
        self.assertTrue(data['title'])
        self.assertTrue(data['detail'])
        self.assertTrue(data['instance'])      

# Make the tests conveniently executable
if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    unittest.main()