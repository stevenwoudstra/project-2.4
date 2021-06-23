from enum import unique
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
#import jwt
import uuid
import datetime
from functools import wraps
import hashlib
from flask_cors import CORS, cross_origin
import sys

from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
cors = CORS(app)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

app.config['SECRET_KEY'] = '1489e0f4ef38021cff66a4a5d1818c76'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
jwt = JWTManager(app)

######JWT code
###tokens decorator 

# def require_token(f):

# 	@wraps(f)
# 	def decorator(*args, **kwargs):
# 		token = None
# 		header = 'x-access-tokens'

# 		if header in request.headers:
# 			token = request.headers[header]
		
# 		if not token:
# 			return {'message': 'no valid token found'}

# 		#try:
# 		print("decodeing")
# 		data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"], verify_exp=True)
# 		user = User.query.filter_by(id=data['id']).first()
# 		# except:
# 		# 	e = sys.exc_info()[0]
# 		# 	print(e)
# 		# 	return {'message': 'invalid'}

# 		return f(user, *args, **kwargs)
# 	return decorator
	
###create token

# def create_token(user_id):

# 	token = jwt.encode(
# 		{
# 			'user_id': user_id,
# 			'exp': datetime.datetime.now() + datetime.timedelta(minutes=3)
# 		},
# 		app.config['SECRET_KEY'], 
# 		"HS256"
# 	)
# 	return token


######hashing
###password

def pass_hash(passwd):
	return hashlib.sha256(bytes(passwd, 'utf-8')).hexdigest()



######app routes
###register
@app.route('/user/register', methods=['POST'])
@cross_origin()
def create_user():
	username = request.json.get("username", None)
	password = pass_hash(request.json.get("password", None))
	email = request.json.get("email", None)
	user = User(
			username = username,
			email = email,
			password = password,
			admin = False
	)
	add_to_ddb(user)
	
	return {'message': 'success'}


###login
@app.route('/user/login', methods=['POST'])
def login():
	username = request.json.get("username", None)
	password = request.json.get("password", None)

	if not username or not password:
		
		return unauthorized('nodata')

	user = get_user(username)
	if user is False:
		return unauthorized('wrong username')

	if user.password == pass_hash(password):
		access_token = create_access_token(identity=username)
		return jsonify(access_token=access_token, user={"roles":"admin"})
	print(user.password)
	print(pass_hash(password))
	return unauthorized('no matching password')
	




###data
@app.route('/user/all', methods=['GET'])
# @require_token
@jwt_required() 
def get_users():
	return {'message': 'TEST OK'}



###401

def unauthorized(wy):
	print(wy)
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
	admin = db.Column(db.Boolean, default=False)

	def __repr__(self):
		return '<User %r>' % self.username

class File(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(256), unique=True, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	type = db.Column(db.String(15))




if __name__ == "__main__":
	app.run(debug=True)
