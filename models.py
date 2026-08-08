from extensions import db




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
    user_id = db.relationship("User_id", backref="User", lazy=True, cascade="all, delete-orphan" )

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey("show.id"), nullable=False)    
    rating = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(300))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)   
    email = db.Column(db.String(50), nullable=False)

    