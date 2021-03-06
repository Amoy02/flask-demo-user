"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from functools import wraps
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import *
from app.models import Users, Likes, Follows, Posts
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import jwt


###
# Routing for your application.
###
#Token Authenticate Decorator
def token_authenticate(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        
        auth = request.headers.get('Authorization', None)
        
        if not auth:
            return jsonify({'error': 'Access Denied : No Token Found'}), 401
        else:
            try:
                userdata = jwt.decode(auth.split(" ")[1], app.config['SECRET_KEY'])
                currentUser = Users.query.filter_by(username = userdata['user']).first()
                
                if currentUser is None:
                    return jsonify({'error': 'Access Denied'}), 401
                
            except jwt.exceptions.InvalidSignatureError as e:
                print (e)
                return jsonify({'error':'Invalid Token'})
            except jwt.exceptions.DecodeError as e:
                print (e)
                return jsonify({'error': 'Invalid Token'})
            return function(*args, **kwargs)
    return decorated_function

###
# Routing for your application.
###

#Registration API route
@app.route('/api/users/register', methods= ['POST'])
def register():
    registerForm = RegisterForm()
    if (request.method == 'POST') and  registerForm.validate_on_submit() :
        
       
            username = request.registerForm['username']
            password = request.registerForm['password']
            firstname =request.registerForm['firstname']
            lastname =request.registerForm['lastname']
            email = request.registerForm['email']
            location = request.registerForm['location']
            biography = request.registerForm['biography']
            file = request.files['profile_photo']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            joined_on = datetime.now()
    
            
            newUser = Users(username= username,password= password,firstname = firstname,lastname= lastname,email= email,location = location,biography= biography,profile_photo=filename,joined_on= joined_on)
            db.session.add(newUser)
            db.session.commit()
            
            # info = [{'username':username, 'password': password,'firstname':firstname,
            # 'lastname':lastname, 'email': email, 'location': location, 'biography': biography,
            # 'photo': filename, 'joined_on': joined_on}]
           
            
            # info = [{'message': "User successfully registered."}]
            return jsonify(message = "User sucessfully  registered.")
        
    return jsonify(error = form_errors(registerForm))

#Logout API Route
@app.route('/api/auth/logout', methods=['GET'])
@token_authenticate
def logout():
    info = [{'message': "User successfully logged out."}]
    return jsonify(info = info) 

#Login API Route
@app.route('/api/auth/login', methods=['POST'])
def login():
    loginForm = LoginForm()
    
    if (request.method == 'POST') and (loginForm.validate_on_submit()):
        username = request.loginForm['username']
        password = request.loginForm['password']
        user = Users.query.filter_by(username = username).first()
        if user is not None and check_password_hash(user.password, password):
            # login_user(user)
            payload = {'user': user.username}
            token = jwt.encode(payload,app.config['SECREY KEY'], algorithm ="HS256")
            info = [{'token': token, 'message': "User successfully logged in."}]
            return jsonify(info = info)
        else:
            # error = [{'error': "Incorrect username or passowrd."}]
            return jsonify(error = "Incorrect username or password.")
            
    return jsonify(form_errors(loginForm))

@app.route('/api/users/<int:user_id>/posts', methods= ['POST'])
# @login_required
@token_authenticate
def add_post(user_id):

        postForm = PostsForm()
        
        if (request.method == 'POST') and (postForm.validate_on_submit()):
            file = request.files['photo']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['POSTS_UPLOAD_FOLDER'], filename))
            user_id = user_id
            caption = request.form['caption']
            created_on = datetime.now()
            
            newpost = Posts(user_id,filename,caption, created_on)
            db.session.add(newpost)
            db.session.commit()
            info = [{'message': "Successfully created a new post"}]
            return jsonify(info = info)
            
        return jsonify(form_errors(postForm))

@app.route('/api/users/<int:user_id>/posts', methods=['GET'])
# @login_required
@token_authenticate
def get_post(user_id):

        allPosts = Posts.query.filter_by(user_id = user_id).all()
        posts = []
        if request.method == 'GET':
            for post in allPosts:
                if post.user_id == user_id:
                    info = {'id': post.id, 'user_id': post.user_id, 'photo': post.photo,
                        'caption': post.caption, 'created_on': post.created_on}
                    posts.append(info)
                return jsonify(posts = posts)   
                
    
@app.route('/api/users/<int:user_id>/follow', methods= ['POST'])
@token_authenticate
def follow(user_id):
    
        request_payload = request.get_json()
        
        query = Follows.query.filter_by(user_id = request_payload['user_id'],
        follower_id = request_payload['follower_id']).first()
        
        if query is not None:
            info = [{'message': "You are not following that user"}]
            return jsonify(info = info)
        
        follow = Follows(request_payload['user_id'], request_payload['follower_id'])
        db.session.add(follow)
        db.session.commit()

        return jsonify(message = "You are now following that user.")
        
    
@app.route('/api/posts', methods = ['GET'])
@token_authenticate
def all_posts():
    
    if (request.method == 'GET'):
        allPosts = db.session.query(Posts).all()
        posts = []
        
        for post in allPosts:
            post = {'id': post.post_id,'user_id': post.user_id, 'photo': post.photo,
            'caption': post.caption, 'created_on': post.created_on}
            posts.append(post)
        return jsonify(posts = posts)
        
    
@app.route('/api/posts/<int:post_id>/like', methods= ['POST'])
@token_authenticate
def like(post_id):
    
    request_payload = request.get_json()
    user_id = request_payload['user_id']
    post_id = request_payload['post_id']
    
    post = Posts.query.filter_by(id = post_id)
    
    if post is None:
        return jsonify(message= "This post does not exist.")
    
    postLikes = Likes.query.filter_by(post_id = post_id).all()
    
    if postLikes is not None:
        for like in postLikes:
            if like.user_id == user_id:
                return jsonify(message= "This post is liked already.")
    
    newLike = Likes(post_id,user_id)
    db.session.add(newLike)
    db.session.commit()

    totalLikes = len(Likes.query.filter_by(post_id = post_id)).all()
    info = [{'message': "Post liked!", 'likes': totalLikes}]
    return jsonify(info = info)



        
# Please create all new routes and view functions above this route.
# This route is now our catch all route for our VueJS single page
# application.
    
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    """
    Because we use HTML5 history mode in vue-router we need to configure our
    web server to redirect all routes to index.html. Hence the additional route
    "/<path:path".
    Also we will render the initial webpage and then let VueJS take control.
    """
    return render_template('home.html')


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

###
# The functions below should be applicable to all Flask apps.
###

# This callback is used to reload the user object from the user ID stored in the session.
# It should take the unicode ID of a user, and return the corresponding user object.
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")