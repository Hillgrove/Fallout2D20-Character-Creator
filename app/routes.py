
from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import RegistrationForm, LoginForm, BackgroundForm, SpecialForm
from app.models import User, Character, Stat, CharacterStat
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password using werkzeug
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to login", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Verify the password using werkzeug
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("index"))
        else:
            flash("Login unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    characters = Character.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", characters=characters)

@app.route("/create_character", methods=["GET", "POST"])
@login_required
def create_character():
    form = BackgroundForm()

    if form.validate_on_submit():
        new_character = Character(
            name=form.name.data,
            origin_id=form.origin_id.data,
            user_id=current_user.id
        )

        db.session.add(new_character)
        db.session.commit()

        return redirect(url_for("choose_specials", character_id=new_character.id))
    
    return render_template("create_character.html", form=form)

@app.route("/choose_specials/<int:character_id>", methods=["GET", "POST"])
@login_required
def choose_specials(character_id):
    character = Character.query.get_or_404(character_id)
    form = SpecialForm()

    if form.validate_on_submit():
        # Loop through each stat and save the selected value
        for stat in Stat.query.all():
            stat_value = request.form.get(f"stat_{stat.id}")
            character_stat = CharacterStat(
                character_id = character.id,
                stat = stat.id, 
                value = stat_value
            )
            db.session.add(character_stat)

            db.session.commit()

        return redirect(url_for("choose_perks", character_id=character.id))
    
    return render_template("choose_specials.html", form=form, character=character, stats=Stat.query.all())
