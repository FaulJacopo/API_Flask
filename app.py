import requests, json, random, string, uuid, urllib.request, array
from functools import wraps
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from routes.auth import auth as bp_auth
from models.conn import db
from models.model import *
from sqlalchemy import desc
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

class ProtectedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))

meme_list = [
    "10-Guy", "1950s-Middle-Finger", "1990s-First-World-Problems", "1st-World-Canadian-Problems", "2nd-Term-Obama",
    "Aaaaand-Its-Gone", "Ace-Primo", "Actual-Advice-Mallard", "Adalia-Rose", "Admiral-Ackbar-Relationship-Expert",
    "Advice-Dog", "Advice-Doge", "Advice-God", "Advice-Peeta", "Advice-Tam", "Advice-Yoda", "Afraid-To-Ask-Andy",
    "Afraid-To-Ask-Andy-Closeup", "Aint-Nobody-Got-Time-For-That", "Alan-Greenspan", "Alarm-Clock", "Albert-Cagestein",
    "Albert-Einstein-1", "Alien-Meeting-Suggestion", "Alright-Gentlemen-We-Need-A-New-Idea", "Always-Has-Been",
    "Alyssa-Silent-Hill", "Am-I-The-Only-One-Around-Here", "American-Chopper-Argument", "Ancient-Aliens",
    "And-everybody-loses-their-minds", "And-then-I-said-Obama", "Angry-Asian", "Angry-Baby", "Angry-Birds-Pig",
    "Angry-Bride", "Angry-Chef-Gordon-Ramsay", "Angry-Chicken-Boss", "Angry-Dumbledore", "Angry-Koala", "Angry-Rant-Randy",
    "Angry-Toddler", "Annoying-Childhood-Friend", "Annoying-Facebook-Girl", "Anri-Stares", "Anti-Joke-Chicken",
    "Apathetic-Xbox-Laser", "Archer", "Are-Your-Parents-Brother-And-Sister", "Are-you-a-Wizard", "Arrogant-Rich-Man",
    "Art-Attack", "Art-Student-Owl", "Arthur-Fist", "Asshole-Ref", "Aunt-Carol", "Austin-Powers-Honestly", "Aw-Yeah-Rage-Face",
    "Awkward-Moment-Sealion", "Awkward-Olympics", "BANE-AND-BRUCE", "BM-Employees", "Babushkas-On-Facebook", "Baby-Cry",
    "Baby-Godfather", "Baby-Insanity-Wolf", "Back-In-My-Day", "Bad-Advice-Cat", "Bad-Joke-Eel", "Bad-Luck-Bear",
    "Bad-Luck-Brian", "Bad-Luck-Hannah", "Bad-Pun-Anna-Kendrick", "Bad-Pun-Dog", "Bad-Wife-Worse-Mom", "Bah-Humbug", "Bane",
    "Bane-Permission", "Barack-And-Kumar-2013", "Barba", "Barbosa-And-Sparrow", "Barney-Stinson-Win", "Baromney", "Baron-Creater",
    "Bart-Simpson-Peeking", "Batman-And-Superman", "Batman-Slapping-Robin", "Batman-Smiles", "Batmobile", "Bazooka-Squirrel",
    "Be-Like-Bill", "Bear-Grylls", "Beard-Baby", "Bebo", "Because-Race-Car", "Ben-Barba-Pointing", "Bender", "Benito",
    "Bernie-I-Am-Once-Again-Asking-For-Your-Support", "Beyonce-Knowles-Superbowl", "Beyonce-Knowles-Superbowl-Face",
    "Beyonce-Superbowl-Yell", "Big-Bird", "Big-Bird-And-Mitt-Romney", "Big-Bird-And-Snuffy", "Big-Ego-Man", "Big-Family-Comeback",
    "Bike-Fall", "Bill-Murray-Golf", "Bill-Nye-The-Science-Guy", "Bill-OReilly", "Billy-Graham-Mitt-Romney", "Bitch-Please",
    "Black-Girl-Wat", "Blank-Blue-Background", "Blank-Colored-Background", "Blank-Comic-Panel-1x2", "Blank-Comic-Panel-2x1",
    "Blank-Comic-Panel-2x2", "Blank-Nut-Button", "Blank-Starter-Pack", "Blank-Transparent-Square", "Blank-Yellow-Sign", "Blob",
    "Blue-Futurama-Fry", "Boardroom-Meeting-Suggestion", "Bonobo-Lyfe", "Booty-Warrior", "Bothered-Bond", "Brace-Yourselves-X-is-Coming",
    "Brian-Burke-On-The-Phone", "Brian-Griffin", "Brian-Williams-Was-There", "Brian-Williams-Was-There-2", "Brian-Williams-Was-There-3",
    "Brian-Wilson-Vs-ZZ-Top", "Britney-Spears", "Bubba-And-Barack", "Buddy-Christ", "Buddy-The-Elf", "Buff-Doge-vs-Cheems", "Bullets",
    "Burn-Kitty", "Business-Cat", "But-Thats-None-Of-My-Business", "But-Thats-None-Of-My-Business-Neutral", "Butthurt-Dweller",
    "CASHWAG-Crew", "CURLEY", "Captain-Hindsight", "Captain-Phillips-Im-The-Captain-Now", "Captain-Picard-Facepalm", "Car-Salesman-Slaps-Hood"
]

admin = Admin(app, name='Admin dashboard', template_mode='bootstrap4')
admin.add_view(ProtectedModelView(User, db.session))
admin.add_view(ProtectedModelView(ApiKey, db.session))

app.register_blueprint(bp_auth, url_prefix='/auth')

migrate = Migrate(app, db)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Chiama init_db durante l'inizializzazione
with app.app_context():
    init_db()

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    # return User.query.get(int(user_id))   # legacy
    return user

@app.route('/')
def home():
    return redirect(url_for('auth.login')) 

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

@app.route('/meme/<text1>&<text2>', methods=["GET"])
def getMeme(text1, text2):
    sent_key = request.headers.get('X-API-Key')

    if not sent_key:
        if not current_user:
            return {'error': 'No API-Key specified'}, 401
        else:
            sent_key = ApiKey.query.filter_by(user_id=current_user.id).first()
            api_key = sent_key
            sent_key = sent_key.value
    else:
        api_key = ApiKey.query.filter_by(value=sent_key).first()
    
    current_app.logger.error(f'API KEY: {api_key}, sent_key:{sent_key}')
    
    if api_key.value == sent_key:
        login_user(api_key.get_user())
        random_meme = random.sample(meme_list, 1)
        text1 = str(text1).replace(" ", "+")
        text2 = str(text2).replace(" ", "+")
        random_meme = (str(random_meme).replace("'", "")).replace('[', "")
        api_request = f"http://apimeme.com/meme?meme={random_meme.replace(']',"")}&top={text1}&bottom={text2}"

        meme = Memes(user_id=api_key.user_id, value=api_request)
        memes = db.session.execute(db.select(Memes).filter_by(user_id=current_user.id)).scalars()
        db.session.add(meme)
        db.session.commit()

        current_app.logger.error(f'URL{api_request}')
        current_app.logger.error(f'API KEY {api_key.value}')
        return render_template('auth/profile.html', api_keys=[api_key], name=api_key.get_user().username.upper(), url_meme=api_request, memes=memes)
    else:
        return {'error': 'Invalid API key'}, 401

if __name__ == '__main__':
    app.run(debug=True)