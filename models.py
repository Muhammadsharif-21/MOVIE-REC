from extensions import db
from flask_login import UserMixin




class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    title = db.Column(db.String(150), nullable=False )
    genre = db.Column(db.String(20))
    status = db.Column(db.String(20), nullable=False)
    poster_url = db.Column(db.String(300))
    plot = db.Column(db.String(500))
    imdb_rating = db.Column(db.String(10))
    year = db.Column(db.String(10))
    reviews = db.relationship("Review", backref="show", lazy=True, cascade="all, delete-orphan")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey("show.id"), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)   
    rating = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(300))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)   
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    shows = db.relationship("Show", backref="user", lazy=True, cascade="all, delete-orphan")
    reviews =db.relationship("Review", backref="user", lazy=True, cascade="all, delete-orphan")