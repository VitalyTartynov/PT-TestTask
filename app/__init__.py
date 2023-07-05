"""
Package for work with blazegraph database using Flask.

Vitaly Tartynov [https://github.com/VitalyTartynov]
"""

from flask import Flask

app = Flask(__name__)

from app import views
