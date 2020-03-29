from flask import Flask, render_template, url_for, redirect, request, session, make_response
from models import *
import time
from sqlalchemy import func
from functools import wraps
import Config
from flask_cors import *
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object(Config)
db.init_app(app)