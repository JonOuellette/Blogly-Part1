"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension   
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'blogly1234'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
app.app_context().push()

connect_db(app)
db.create_all()


@app.route('/')
def user_list():
    
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/new', methods = ["GET"])
def new_user_form():

    return render_template('/new.html')

@app.route('/new', methods = ["POST"])
def new_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form['image_url'] or None

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

@app.route("/<int:user_id>")
def show_user(user_id):
    
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route("/<int:user_id>/edit")
def edit_user(user_id):
    user= User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route("/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    user= User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    return redirect("/")

@app.route("/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user= User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')