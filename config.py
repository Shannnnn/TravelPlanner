from flask import Flask
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

dbstring = 'postgresql://postgres:imawesome@127.0.0.1:5432/travelplannerdb'