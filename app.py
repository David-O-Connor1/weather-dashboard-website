from flask import Flask,render_template,redirect,url_for,session,g,request,flash
from forms import RegistrationForm,LoginForm,CityWeatherForm
from database import get_db,close_db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_session import Session
from functools import wraps
from datetime import datetime
import requests

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "my_secret_key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

api_key = "ced06c211ddd53a84a7cda43da0e6dba"

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id",None)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            flash("Please log in to access that page","error")
            return redirect(url_for("login",next = request.url))
        return view(*args, **kwargs)
    return wrapped_view

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard",methods=["GET","POST"])
@login_required
def dashboard():
    error = None
    weather = None
    form = CityWeatherForm()
    if form.validate_on_submit():
        city = form.city.data
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get("https://api.openweathermap.org/data/2.5/weather",params=params)

        if response.status_code == 200:
            data = response.json()
            weather = {
                "city": city,
                "temperature": data["main"]["temp"],
                "humidity":data["main"]["humidity"],
                "condition":data["weather"][0]["description"]
            }
        else:
            error = "city not found"
    return render_template("dashboard.html",error=error,weather=weather,form=form)

@app.route("/register",methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = form.user.data
        password = form.password.data
        db = get_db()
        conflict = db.execute("""SELECT * FROM users WHERE username = ?""",(user,)).fetchone()

        if conflict is not None:
            form.user.errors.append("Username conflicts with another")
        else:
            db.execute("""INSERT INTO users(username,password) VALUES (?, ?)""",(user,generate_password_hash(password)))
            db.commit()
            flash("Registration successful! Please log in","success")
            return redirect(url_for("login"))
    return render_template("register.html",form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.user.data
        password = form.password.data
        db = get_db()
        matching_user = db.execute("""SELECT * FROM users WHERE username = ?""",(user,)).fetchone()
        if matching_user is None:
            form.user.errors.append("Unknown user id")
        elif not check_password_hash(matching_user["password"],password):
            form.password.errors.append("Incorrect password")
        else:
            session.clear()
            session["user_id"] = matching_user["id"]
            flash("Logged in successfully!","success")
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("home")
            return redirect(next_page)
    return render_template("login.html",form=form)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out","success")
    return redirect(url_for("home"))

    