from enum import unique
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
import jwt
import uuid
import datetime
from functools import wraps
import hashlib

app = Flask(__name__)

app.config['SECRET_KEY'] = '1489e0f4ef38021cff66a4a5d1818c76'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


######JWT code
###tokens decorator 

def require_token(f):

	@wraps(f)
	def decorator(*args, **kwargs):
		token = None
		header = 'x-access-tokens'

		if header in request.headers:
			token = request.headers[header]
		
		if not token:
			return {'message': 'no valid token found'}

		try:
			data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
			user = User.query.filter_by(id=data['id']).first()
		except:
			return {'message': 'valid'}

		return f(user, *args, **kwargs)
	return decorator
	
###create token

def create_token(user_id):

	token = jwt.encode(
		{
			'user_id': user_id,
			'exp': datetime.datetime.now() + datetime.timedelta(minutes=120)
		},
		app.config['SECRET_KEY'], 
		"HS256"
	)
	return token


######hashing
###password

def pass_hash(passwd):
	return hashlib.sha256(bytes(passwd, 'utf-8')).hexdigest()



######app routes
###register
@app.route('/user/register', methods=['POST'])
def create_user():
	req_data = request.get_json()

	user = User(
			username = req_data['user_name'],
			email = req_data['email'],
			password = pass_hash(req_data['password']),
	)
	add_to_ddb(user)
	return {'message': 'success'}


###login
@app.route('/user/login', methods=['POST'])
def login():
	user_data = request.authorization

	if not user_data or not user_data.username or not user_data.password:
		return unauthorized()

	user = get_user(user_data.username)
	if user is False:
		return unauthorized()

	if user.password is pass_hash(user_data.password):
		token = create_token(user.id)
		return jsonify({'token': token})

	return unauthorized()
	




###data
@app.route('/user/all', methods=['GET'])
@require_token
def get_users():
	return {'message': 'TEST OK'}



###401

def unauthorized():
	return make_response('faild to login', 401, {'Authentication': 'FAILD'})


######ddb code
### ddb functions

def add_to_ddb(new_object):
	db.session.add(new_object)
	db.session.commit()


def get_user(username):
	user = User.query.filter_by(username=username).first()
	if not user:
		return False
	return user



###ddb classes
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(64), nullable=False)

	def __repr__(self):
		return '<User %r>' % self.username

class File(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(256), unique=True, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	type = db.Column(db.String(15))




if __name__ == "__main__":
	app.run(debug=True)
