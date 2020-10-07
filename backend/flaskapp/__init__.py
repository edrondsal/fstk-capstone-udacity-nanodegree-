import os
import random
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Roles, Actors
from responses import Response



def create_app(test_config=None):
    return True
