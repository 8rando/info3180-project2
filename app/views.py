"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, jsonify, send_file,send_from_directory, g
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from app.forms import PostForm, LoginForm, signUpForm, FollowForm
from app.models import Post, Users, Likes, Follow
import os,jwt 
from datetime import datetime, timedelta



###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})



@app.route("/api/v1/generate-token")
def generate_token():
    timestamp = datetime.UTC
    # do i update to have username and password?
    payload = {
        "sub": 1,
        "iat": timestamp,
        "exp": timestamp + timedelta(hours=24)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return token

@app.route('/api/v1/register',methods=["POST"])
def register():
    form = signUpForm()
    if request.method == "POST" and form.validate_on_submit():
        username =form.username.data
        password = form.password.data
        first_name = form.firstName.data
        last_name = form.lastName.data
        email = form.email.data
        location = form.location.data
        biography = form.biography.data
        profile_photo = form.photo.data
        filename = secure_filename(profile_photo.filename)
        user = Users(username, password, first_name, last_name, email, location, biography, filename)
        profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': f"Account was successfully created for {username}!!"})
    else:
        db.session.rollback()
        formErrors = form_errors(form)
        errors = {
            "errors": formErrors
        }
        return jsonify(errors)
    
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    form = LoginForm()
    message = ''
    if request.method == "POST":
        if form.validate_on_submit():
            # Get the username and password values from the form.
            username = form.username.data
            password = form.password.data
            user = db.session.execute(db.select(Users).filter_by(username=username)).scalar()
            if user is not None and (check_password_hash(user.password, password)):
                # Gets user id, load into session
                login_user(user)
                message = {'token': generate_token()}
            else:
                message = {'errors': ['Username or password not correct']}
        else:
            errors = form_errors(form)
            if (errors):
                error_list = {"errors": []}
                error_list['errors'] = errors
                message = error_list
      
        return jsonify(message)

@app.route('/api/v1/currentuser', methods=['GET'])
def get_user():  
    response = '' 
    if current_user.is_authenticated:
        user = current_user
        response = {'message': user.get_id()}      
    else:    
        response = {'Error': 'User is not logged in'}

    return jsonify(response) 

@app.route('/api/v1/users/<user_id>', methods=['GET'])
@login_required

def getUserDetails(user_id):
    user = Users.query.filter_by(id=user_id).first()
    
    user_data = {
        "id": user.id,
        "username": user.username,
        "firstname": user.first_name,
        "lastname": user.last_name,
        "email": user.email,
        "location": user.location,
        "biography": user.biography,
        "profile_photo": "/api/v1/photos/{}".format(user.profile_photo),
        "joined_on": user.joined_on
    }
    return jsonify(user_data) 
        
   

@app.route("/api/v1/auth/logout", methods=['POST'])
@login_required
def logout():
    
    logout_user()
    
    message = {'success':'Successfully logged out'}
    
    return jsonify(message)
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

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


#   Adding a new post for a user
@app.route('/api/v1/users/<int:user_id>/posts', methods=['POST'])
@login_required
def add_post(user_id):
    if current_user.id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    form = PostForm()

    if form.validate_on_submit():
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_post = Post(user_id=user_id, caption=form.caption.data, photo=filename, created_on=datetime.now())
        db.session.add(new_post)
        db.session.commit()

        return jsonify({
            'message': 'Post successfully added',
            'post': {
                'id': new_post.id,
                'caption': new_post.caption,
                'photo': filename,
                'user_id': user_id,
                'created_on': new_post.created_on
            }
        }), 201

    else:
        return jsonify({'errors': form_errors(form)}), 400
    
#   Returning user's posts
@app.route('/api/v1/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    #   post or posts???
    posts = Post.query.filter_by(user_id=user_id).all()
    posts_list = [{
        'id': post.id,
        'caption': post.caption,
        'photo': post.photo,
        'created_on': post.created_on.strftime('%Y-%m-%d %H:%M:%S')
    }for post in posts]

    return jsonify(posts_list), 200

#   Returning all posts for all Users
@app.route('/api/v1/posts', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()
    post_list = [{
        'id': post.id,
        'user_id': post.user_id,
        'caption': post.caption,
        'photo': post.photo,
        'created_on': post.created_on.strftime('%Y-%m-%d %H:%M:%S')
    }for post in posts]

    return jsonify(post_list), 200

#   Creating a Follow relationship
@app.route('/api/users/<int:target_id>/follow', methods=['POST'])
@login_required
def follow_user(user_id):
    if current_user.id == target_id:
        return jsonify({'error': 'You cannot follow yourself'}), 403
    
    follow = Follow.query.filter_by(user_id=current_user.id, target_id = target_id).first()
    if follow:
        return jsonify({'message': 'Already following this user'}), 409
    
    new_follow = Follow(user_id=current_user.id, target_id=target_id)
    db.session.add(new_follow)
    db.session.commit()

    return jsonify({'message': 'User followed'}), 201

@app.route('/api/v1/users/<user_id>/follow', methods=['GET'])
@login_required
#@requires_auth
def getFollowers(user_id):
    
    if request.method == 'GET':
        
        # count = 0
    
        followers = Follow.query.filter_by(target_id=user_id).all()
        followers_list = []

        for follow in followers:
            # count += 1
            followers_list.append(follow_user.user_id)
            
        
        
        data = {"followers": followers_list}
        return jsonify(data)


#   Setting a Like on the Current Post by the Logged-in User
@app.route('/api/v1/posts/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    like = Likes.query.filter_by(post_id=post_id, user_id=current_user.id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'message': 'Post liked'}), 201
    else:
        new_like = Likes(post_id=post_id, user_id=current_user.id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify({'message': 'Post like'}), 201
    

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404