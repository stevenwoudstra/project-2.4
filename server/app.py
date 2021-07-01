from enum import unique
from sys import path
from flask import Flask, request, jsonify, make_response, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
#import jwt
import uuid
from datetime import date, timedelta, timezone, datetime
from functools import wraps
import hashlib
from flask_cors import CORS, cross_origin
import os
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
import json, time

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity


#export FLASK_ENV=development
app = Flask(__name__)
cors = CORS(app, resources=r'/*')

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

app.config['SECRET_KEY'] = '1489e0f4ef38021cff66a4a5d1818c76'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
#app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
app.config['UPLOAD_FOLDER'] = './Files'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}

db = SQLAlchemy(app)
jwt = JWTManager(app)

######JWT code

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None

### file code
def allowed_file(filename):
	print('.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)
	return ('.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

def save_file_to_ddb(user, url, type):

	file = File(
				url = url,
				user_id = user.id,
				type=type
				)
	
	db.session.add(file)
	user.files.append(file)
	db.session.commit()
	return file

def get_file_by_id(id):
	return File.query.filter_by(id=id).first()

def create_file_name(filename):
	file_type = filename.rsplit('.', 1)[1]
	return str(time.time()).replace('.', '') + '.' + file_type 


def get_file_users(form):
	users = dict(form).get('users').split(",")
	user_list = []
	for u in users:
		print(u)
		if get_user_by_name(u):
			user_list.append(get_user_by_name(u))

	return user_list
	

### jwt routes

@app.route("/user/refresh", methods=["POST"])
@cross_origin()
@jwt_required(refresh=True)
def refresh():
	identity = get_jwt_identity()
	access_token = create_access_token(identity=identity)
	refresh_token = create_refresh_token(identity=identity)
	return jsonify(access_token=access_token, refresh_token=refresh_token)

@app.route("/user/logout", methods=["DELETE"])
@cross_origin()
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify(msg="JWT revoked")
	


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
@cross_origin()
def login():
	username = request.json.get("username", None)
	password = request.json.get("password", None)
	role = "user"

	if not username or not password:
		return unauthorized('nodata')

	user = get_user_by_name(username)

	if user is False:
		return unauthorized('wrong username')

	if user.password == pass_hash(password):
		access_token = create_access_token(identity=user.id)
		refresh_token = create_refresh_token(identity=user.id)
		return jsonify(access_token=access_token, refresh_token=refresh_token, user={"id":user.id})

	print(user.password)
	print(pass_hash(password))
	return unauthorized('no matching password')
	
######
#logout is at JWT code just accept it
######

######
#file upload
######
@app.route('/file/upload/profile', methods=['POST'])
@cross_origin()
@jwt_required() 
def upload_profile_picture():
	if 'file' not in request.files:
		return {'error':'no file'}

	file = request.files['file']
	print(file.filename)
	if not allowed_file(file.filename):
		return {'error':'wrong file type'}

	file_name = create_file_name(secure_filename(file.filename))
	file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id))
	full_path = os.path.join(file_path, file_name)

	if os.path.exists(file_path) is False:
		os.mkdir(file_path)

	# print(file_path)
	file.save(full_path)
	# print(request.__dir__())
	
	profile_pic = save_file_to_ddb(user = current_user, url=full_path, type="ProfilePic")
	current_user.profile_picture = profile_pic.id
	db.session.commit()
	return {"message":"oke", "picture_id": profile_pic.id}

@app.route('/file/upload', methods=['POST'])
@cross_origin()
@jwt_required()
def upload_file():
	if 'file' not in request.files:
		return {'error':'no file'}

	file = request.files['file']
	if not allowed_file(file.filename):
		return {'error':'wrong file type'}

	# print(request.json)
	file_name = create_file_name(secure_filename(file.filename))
	file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id))
	full_path = os.path.join(file_path, file_name)
	if os.path.exists(file_path) is False:
		os.mkdir(file_path)
	
	file.save(full_path)
	
	saved_file = save_file_to_ddb(user = current_user, url=full_path, type="file")
	user_list = get_file_users(dict(request.form))
	for user in user_list:
		user.files.append(saved_file)
	db.session.commit()
	return {"message":"oke", "picture_id": saved_file.id}


###data
@app.route('/user/all', methods=['GET'])
@cross_origin()
@jwt_required() 
def get_users():
	return {'message': 'TEST OK'}


@app.route("/user/profile", methods=['GET'])
@cross_origin()
@jwt_required()
def get_user_profile():
	user = current_user
	if not user:
		return make_response('faild to find user', 404)
	return {
			"first_name": user.first_name,
			"last_name": user.last_name,
			"bio": user.bio,
			"profile_picture": user.profile_picture,
			"email":user.email
			}

@app.route("/user/profile/update", methods=['POST'])
@cross_origin()
@jwt_required()
def update_user_profile():
	user = current_user
	if not user:
		return make_response('faild to find user', 404)
	email = request.json.get("email", None)
	first_name = request.json.get("first_name", None)
	last_name = request.json.get("last_name", None)
	user.email = email
	user.first_name = first_name
	user.last_name = last_name
	db.session.commit()
	return {'message': 'success'}
	
	

@app.route("/user/info", methods=['GET'])
@cross_origin()
@jwt_required()
def get_user():
	user = current_user
	role = "user"
	picture_is_set = False
	if not user:
		return make_response('faild to find user', 404)
	if user.admin is True:
		role = "admin"
	if user.profile_picture:
		picture_is_set = True
	return { "user":{
				"userid":user.id,
				"username":user.username,
				"email":user.email,
				"role":role,
				"picture":picture_is_set
				}
			}

@app.route("/user/profile/picture", methods=['GET'])
@cross_origin()
@jwt_required()
def get_profile_picture():
	user = current_user
	file = get_file_by_id(current_user.profile_picture)
	file_info = file.meta_data()
	print(file_info)
	return send_from_directory(	
								file_info['path'], 
								filename = file_info['name'], 
								as_attachment = True,
								)


###401

def unauthorized(wy):
	print(wy)
	return make_response({'Authentication': wy}, 401)

####### general http error logging
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response




######ddb code
### ddb functions

def add_to_ddb(new_object):
	db.session.add(new_object)
	db.session.commit()


def get_user_by_name(username):
	user = User.query.filter_by(username=username).first()
	if not user:
		return False
	return user

def get_user_by_id(id):
	user = User.query.filter_by(id=id).first()
	if not user:
		return False
	return user



###ddb tabels
shares = db.Table( 
				'shares',
				db.Column(
						'user_id',
						db.Integer,
						db.ForeignKey('user.id', ondelete="cascade"),
						primary_key=True
				),
				db.Column(
						'file_id',
						db.Integer,
						db.ForeignKey('file.id', ondelete="cascade"),
						primary_key=True
				),
				)

###ddb classes
###app
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(64))
	first_name = db.Column(db.String(64))
	last_name = db.Column(db.String(64))
	bio = db.Column(db.String(256))
	profile_picture = db.Column(db.Integer, db.ForeignKey('file.id'))
	admin = db.Column(db.Boolean, default=False)
	files = db.relationship('File',
							secondary=shares,
							backref=db.backref('users', lazy=True)
							)

	def __repr__(self):
		return '<User %r>' % self.username

class File(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(256), unique=True, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	type = db.Column(db.String(15))

	def __repr__(self):
		return '<File %r>' % self.url

	def meta_data(self):
		url_list = self.url.split("/")
		name = url_list.pop()
		path = '/'.join(url_list)
	
		return {"name": name, "path": path, "full_path": self.url}


###JWT
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

if __name__ == "__main__":
	app.run(debug=True)




# def code for testing in shell
# file = File.query.one_or_none()
# user = User.query.one_or_none()
################################
