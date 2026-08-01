from flask import Flask
from extensions import db, api
app = Flask(__name__)
import resources

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:ariari@127.0.0.1:3306/moviedb"
db.init_app(app)
api.init_app(app)

from models import Show, Review


@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)