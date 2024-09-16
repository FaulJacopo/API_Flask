from geopy.geocoders import Nominatim
from flask_login import LoginManager
import requests, json
from flask import Flask, render_template, request
from routes.auth import auth as bp_auth
from models.conn import db
from models.model import *
from flask_migrate import Migrate

app = Flask(__name__)
app.register_blueprint(bp_auth, url_prefix='/auth')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_API_adm:Admin$00@localhost/flask_meteoAPI'
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/createuser', methods=["POST"])
#def create_user(username, email, password):
def create_user():
    values = request.json
    username = values['username']
    email = values['email']
    password = values['password']
    user = User(username=username, email=email)
    user.set_password(password)  # Imposta la password criptata
    db.session.add(user)  # equivalente a INSERT
    db.session.commit()
    return (f"Utente {username} creato con successo.")

def find_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    return user

def test_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)

    # Verifica della password
    userChecked = find_user_by_username(username)
    return user.check_password(userChecked.password)

def add_request_to_DB(request):
    request = Request(request=request)
    db.session.add(request)
    db.session.commit()
    return "Aggiunto correttamente"

@app.route('/weather', methods=["POST"])
def weather_single():
    values = request.json
    city = values["city"]
    return weather(city)

@app.route('/weather/<city>')
def weather(city):
    add_request_to_DB(city)

    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    latitude = location.latitude
    longitude = location.longitude

    headers = {'Content-type': 'Application/json'}
    requestPost = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
    res = requests.post(requestPost, headers=headers)
    return f"{res.json()}"

@app.route('/hello/<username>')
def hello(username):
    return render_template('home.html', username=username)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    # return User.query.get(int(user_id))   # legacy
    return user

if __name__ == '__main__':
    app.run(debug=True)