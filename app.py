from flask import Flask, render_template
from extensions import db, api, bcrypt, Login_manager
from dotenv import load_dotenv


load_dotenv()
from flask_migrate import Migrate

app = Flask(__name__)
import resources

migrate = Migrate(app, db)

app.config["SECRET_KEY"] = "mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:ariari@127.0.0.1:3306/moviedb"
)
db.init_app(app)
api.init_app(app)
bcrypt.init_app(app)
Login_manager.init_app(app)


from models import Show, Review, User

#Flask login loads user data from db to User object using this function
@Login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
