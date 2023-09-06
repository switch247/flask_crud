from flask import Blueprint, jsonify, request,flash,abort,redirect,url_for
from app import db
import json
# from app.models import user.User, employee.Employee ...
from models import User


main = Blueprint('main', __name__)





@main.route('/check_db_connection')
def hello():
    return 'hello'
# create
# @main.route('/')
# def create():
#     data = request.get_json()
#     User
#     User.query.all

# # update
# @main.route('/<id>')
# def update(id):
#     pass

# # delete
# @main.route('/<id>')
# def delete(id):
#     pass


# # read
# @main.route('/')
# def read():
#     pass


# @main.route('/<id>')
# def create():
#     pass


