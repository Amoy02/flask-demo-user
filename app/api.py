#Amoy Patterson and Abigail Miles 

"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import sys
import os
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from werkzeug.utils import secure_filename
# from flask_login import LoginManager
# from . import db


app = Flask(__name__)
app.config['SECRET_KEY'] = "supersecret"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://photogram:photogram@localhost/photogram"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 

POSTS_UPLOAD_FOLDER = "./app/static/posts_photos"

db = SQLAlchemy(app)

# #flask login mananger 
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

app.config.from_object(__name__)


class Users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    email = db.Column(db.String(60))
    location = db.Column(db.String(30))
    biography = db.Column(db.String(300))
    profile_photo = db.Column(db.String(100))
    joined_on = db.Column(db.String(10))

    def __init__(self, username,password, firstname, lastname, email,location, biography): #profile_photo, joined_on 
        self.username = username       
        self.password = generate_password_hash(password, method = 'pbkdf2:sha256')
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.location = location
        self.biography = biography
        # self.profile_photo = profile_photo
        # self.joined_on = joined_on

class Posts(db.Model):
    __tablename__='posts'
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer)
    photo = db.Column(db.String(100))
    caption = db.Column(db.String(100))
    created_on = db.Column(db.String(10))

    def __init__(self,user_id,photo,caption,created_on):
        self.user_id = user_id
        self.photo = photo
        self.caption = caption
        self.created_on = created_on

class Likes(db.Model):
    __tablename__='likes'
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)

    def __init__(self,user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id


    
class Follows(db.Model):
    __tablename__='follows'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    follower_id = db.Column(db.Integer)

    def __init__(self,user_id, follower_id):
        self.user_id = user_id
        self.follower_id = follower_id


#registration
@app.route("/api/users/register", methods=['POST'])
def register():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    user = Users(username=data['username'], password=hashed_password, 
        firstname = data['firstname'], 
        lastname = data['lastname'],  
        email = data['email'], 
        location = data['email'],
        biography = data['biography']),
        # profile_photo = data['profile_photo'],
        # joined_on = data['joined_on']

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User successfully registered"})

#login 
@app.route("/api/auth.login", methods = ['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm = "Login Required"'})
    if check_password_hash(user.password, data["password"]):
        token = jwt.encode({'id':user.id}, app.config['SECRET_KEY'])
        return jsonify({"token": token.decode('utf-8')})
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm = "Login Required'})

#logout
@app.route('/api/auth/logout', methods = ['GET'])
def logout():
    data = [{'message': "User successfully logged out."}]
    return jsonify(data = data)

#posts 
@app.route('/api/users/<int:user_id>/posts', methods = ['POST'])
def add_post(user_id):
    data = CreatePostForm()
    if(request.methods == 'POST') and (data.validate_on_submit()):
        file = request.files['photo']
        filename = secure_filename(file.filename)
        file.save(os.path.join('./app', app.config['POSTS_UPLOAD_FOLDER'], filename))
        user_id - user_id
        caption = request.form['caption']
        created_on = datetime.now()

        new = Posts(user_id, filename, caption, created_on)
        db.session.add(new)
        db.session.commit()
        info = [{'message': "Successfully created a new post"}]
        return jsonify(info = info)
    return jsonify(form_erros(data))



if __name__ == '__main__':
    app.run(debug=True)

