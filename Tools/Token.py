from flask import Flask, jsonify,  current_app, request
from flask_pymongo import PyMongo
from itchat.storage import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask_sqlalchemy import SQLAlchemy
from models import *


def generate_token(api_users):
    expiration = 3600*24*7
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration) #expiration是过期时间
    token = s.dumps({'id': api_users}).decode('ascii')
    return token


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token,but expired
    except BadSignature:
        return None  # invalid token
    user = Users.query.filter(Users.user_id==data['id']).first()
    return user