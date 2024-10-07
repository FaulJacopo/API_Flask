#auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, Flask, app
from flask import current_app   # definisce il contesto del modulo
from flask_login import login_user, login_required, logout_user, current_user  # https://flask-login.readthedocs.io/en/latest/#flask_login.login_user
import uuid, random
from models.conn import db
from models.model import *

auth = Blueprint('auth', __name__)

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

@auth.route('/login', methods=['GET'])
def login():
    # shows the login form page
    return render_template('auth/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # manages the login form post request
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    stmt = db.select(User).filter_by(email=email)
    user = db.session.execute(stmt).scalar_one_or_none()
    # user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    current_app.logger.info(f'user {user}')
    if not user or not user.check_password(password):
        current_app.logger.error(f' user {email} not logged with password {password}')
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    flash("You are now logged in!")
    login_user(user, remember=remember)
    return redirect(url_for('auth.base'))

@auth.route('/home')
@login_required
def base():
    return render_template('home.html') 

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are successfully logout from this page!")
    return render_template('auth/login.html')

@auth.route('/profile')
@login_required
def profile():
    api_keys = (User.query.filter_by(email=current_user.email).first()).get_api_keys()
    memes = db.session.execute(db.select(Memes).filter_by(user_id=current_user.id)).scalars()
    name = current_user.username.upper()
    return render_template('auth/profile.html', api_keys=api_keys, name=name, url_meme=None, memes=memes)

@auth.route('/signup', methods=["GET"])
def signup():
    return render_template('auth/signup.html')

@auth.route('/generate_meme', methods=["POST"])
def generate_meme():
    upper_text = request.form["upper_text"]
    lower_text = request.form["lower_text"]

    if not upper_text:
        upper_text = "upper_text"
    if not lower_text:
        lower_text = "lower_text"
    return redirect(url_for('getMeme', text1=upper_text, text2=lower_text))

@auth.route('/signup', methods=['POST'])
def signup_post():
    # signup input validation and logic
    #TODO verify password strenght
    username = request.form["username"]
    email = request.form["email"]    
    password = request.form["password"]

    if not username:
        flash('Invalid username')
        return redirect(url_for('auth.signup'))
    if not email:
        flash('Invalid email')
        return redirect(url_for('auth.signup'))
    if not password:
        flash('Invalid password')
        return redirect(url_for('auth.signup'))                
    
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    if user: 
        flash('User with this email address already exists')
        return redirect(url_for('auth.signup'))
    
    api_key = str(uuid.uuid4())

    user = User(username=username, email=email)
    user.set_password(password)  # Imposta la password criptata
    user.set_api_key(api_key) # Imposta la nuova API Key
    db.session.add(user)  # equivalente a INSERT
    db.session.commit()

    flash("You are now registered in this website!")
    return redirect(url_for('auth.login'))
