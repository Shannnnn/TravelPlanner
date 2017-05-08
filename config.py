from flask import Flask
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)