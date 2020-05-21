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
app.config['SECRET_KEY'] =  "v\xf9\xf7\x11\x13\x18\xfaMYp\xed_\xe8\xc9w\x06\x8e\xf0f\xd2\xba\xfd\x8c\xda"

#heroku postgresql 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://seqydqeaosgiaa:94fab157e29ee4ed6357ad9578a400112316d3fd333a724de5d5ae1a5d110568@ec2-18-235-20-228.compute-1.amazonaws.com:5432/d3hh7qka0td7gv"

#postgres
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

    def __init__(self, username,password, firstname, lastname, email,location, biography, profile_photo, joined_on):  
        self.username = username       
        self.password = generate_password_hash(password, method = 'pbkdf2:sha256')
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.location = location
        self.biography = biography
        self.profile_photo = profile_photo
        self.joined_on = joined_on

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

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None 

        if 'x-auth-token' in request.headers:
            token = request.headers['x-auth-token']
        if not token:
            return jsonify({'message': 'Token is missing!'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = users.query.filter_by(
                id = data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated 

@app.route("/api/auth", methods = ['GET'])
def load_user():
    token = None 
    current_user = None 

    if 'x-auth-token' in request.headers:
        token = request.headers['x-auth-token']
    if not token:
        return make_response("Not found", 404)
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        current_user = Users.query.filter_by(
            id = data['id']).first()
    except:
        return jsonify({'message': 'Token is invalid'}), 401 
    if current_user != None:
        try:
            user = {
                "username": current_user.username,
                "id": current_user.id,
                "firstname": current_user.firstname,
                "lastname": current_user.lastname,
                "email": current_user.email,
                "biography": current_user.biography,
                "profile_photo": current_user.profile_photo,
                "joined_on": current_user.joined_on
            }
            return jsonify({"user": user})
        except Exception as e:
            print(e)
            return make_response("Not found", 404)
    else:
        raise Exception 
        return make_response("Not found", 404)

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
@token_required
def logout():
    data = [{'message': "User successfully logged out."}]
    return jsonify(data = data)

#get posts 
@app.route("/api/users/<user_id>/posts", methods = ['GET'])
@token_required 
def get_posts(user_id):
    posts = Posts.query.filter_by(user_id = user_id).all()
    output = []
    for post in posts:
        user = Users.query.filter_by(user_id = post.user_id).first()
        post_data = {
            'id': post.id,
            'user': user,
            "photo": post.photo,
            "caption": post.caption,
            "created": post.created_on
        }
        output.append(post_data)
    return jsonify({"posts": output})

#create post 
@app.route("/api/users/<user_id>/posts", methods = ['POST'])
@token_required 
def create_post(user_id):
    file = request.files["photo"]
    caption = request.form["caption"]
    filename = secure_filename(file.filename)
    file.save(os.path(app.config['UPLOAD_FOLDER'], filename))

    db.session.add(post)
    db.session.commit()

    json_post = {
        "caption":post.caption,
        "user_id": post.user_id,
        "id": post.id,
        "created_on": post.created_on,
        "photo": post.photo
    }
    return jsonify(json_post)

#follow 
@app.route("/api/users/<user_id>/follow", methods = ['POST'])
@token_required
def follow(current_user, user_id):
    follow = Follows(user_id = user_id, follower_id = current_user)
    db.session.add(follow)
    db.session.commit()
    return jsonify({"message": "Followed"})

#all posts 
@app.route("/api/posts",methods = ['GET'])
@token_required
def getall_posts():
    posts = Posts.query.all()
    output = []
    for post in posts:
        user = Users.query.filter_by(id = post.user_id).first()
        username = user.username
        likes = get_likes(post.id)
        post_data = {
            'id': post.id,
            'user': username,
            "photo": post.photo,
            "description": post.caption,
            "created_on": post.created_on,
            "likes": likes 
        }
        output.append(post_data)
    return jsonify({"posts": output})

def get_likes(post_id):
    likes = Likes.query.filter_by(post_id = post_id).all()
    output = []
    for like in likes:
        likee = {
            "user": like.user_id,
            "post": like.post_id,
            "id": like.id 
        }
        output.append(likee)
    return output

#like 
@app.route("/api/posts/<post_id>/like", methods = ['POST'])
@token_required
def like(current_user, post_id):
    check = Likes.query.filter_by(
        post_id = post_id, user_id = current_user.id).first()
    if not check:
        like = Likes(user_id = current_user.id, post_id = post_id)
        db.session.add(like)
        db.session.commit()
        return jsonify({"like": like_id})
    else:
        return make_response("Already liked", 401)


#all new routes above here 

def form_errors(form):
    error_messages = []
    for field, errors in form.errorss.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            )
            error_messages.append(message)
    return error_messages 

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatiable'] = 'IE = Edeg, chrome = 1'
    response.headers['Cache-Control'] = 'public, max-age =0'
    return response 

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True)

