"""
Package for work with blazegraph database using Flask.

Vitaly Tartynov [https://github.com/VitalyTartynov]
"""

from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app, title='PT-TestTask', doc='/api/v1')

from app import views
