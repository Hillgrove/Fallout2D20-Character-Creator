
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.forms import RegistrationForm, LoginForm, BackgroundForm, SpecialForm, PerkForm, DeleteForm, SkillForm
from app.models import User, Character, Stat, CharacterStat, Perk, CharacterPerk, Skill, CharacterSkill
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
    delete_form = DeleteForm()
    return render_template("dashboard.html", characters=characters, form=delete_form)

@app.route("/delete_character/<int:character_id>", methods=["POST"])
@login_required
def delete_character(character_id):
    character = Character.query.get_or_404(character_id)
    db.session.delete(character)
    db.session.commit()
    flash("Character successfully deleted", "success")
    return redirect(url_for("dashboard"))

# @app.route("/edit_character/<int:character_id>", methods=["POST"])
# @login_required
# def edit_character(character_id):
#     character = Character.query.get_or_404(character_id)
#     form = CharacterForm(obj=character)

#     if form.validate_on_submit():
#         form.populate_obj(character)
#         db.session.commit()
#         flash("Character updated successfully", "success")
#         return redirect(url_for("dashboard"))
    
#     return render_template("edit_character.html", form=form, character=character)

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

    if request.method == "POST":
        app.logger.info("POST request received")
        if form.validate_on_submit():
            app.logger.info("Form validated successfully")
            try:
                # Remove existing CharacterStat entries for the character to avoid duplicates
                CharacterStat.query.filter_by(character_id=character.id).delete()

                # Create a list of the form data to handle each stat
                stats = {
                    "Strength": form.strength.data,
                    "Perception": form.perception.data,
                    "Endurance": form.endurance.data,
                    "Charisma": form.charisma.data,
                    "Intelligence": form.intelligence.data,
                    "Agility": form.agility.data,
                    "Luck": form.luck.data
                }

                # Loop through each stat and save the selected value
                for stat_name, stat_value in stats.items():
                    stat = Stat.query.filter_by(name=stat_name).first()
                    if stat:
                        character_stat = CharacterStat(
                            character_id=character.id,
                            stat_id=stat.id,
                            value=stat_value
                        )
                        db.session.add(character_stat)

                db.session.commit()
                return redirect(url_for("choose_perks", character_id=character.id))
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error saving stats: {e}")
                flash("An error occurred while saving your stats. Please try again.", "danger")
        else:
            app.logger.warning("Form validation failed")
            for field, errors in form.errors.items():
                for error in errors:
                    app.logger.warning(f"Validation error in {field}: {error}")
            flash("Please correct the errors in the form and resubmit.", "danger")

    return render_template("choose_specials.html", form=form, character=character, stats=Stat.query.all())

@app.route("/choose_perks/<int:character_id>", methods=["GET", "POST"])
@login_required
def choose_perks(character_id):
    character = Character.query.get_or_404(character_id)
    form = PerkForm()

    if form.validate_on_submit():
        selected_perks = request.form.getlist("perks")
        for perk_id in selected_perks:
            character_perk = CharacterPerk(
                character_id=character.id,
                perk_id=perk_id
            )
            db.session.add(character_perk)

        db.session.commit()

        return redirect(url_for("choose_skills", character_id=character.id))
    
    return render_template("choose_perks.html", form=form, character=character, perks=Perk.query.all())

@app.route("/choose_skills/<int:character_id>", methods=["GET", "POST"])
@login_required
def choose_skills(character_id):
    character = Character.query.get_or_404(character_id)
    form = SkillForm()
    
    # Populate the skill choices
    form.skills.choices = [(skill.id, skill.name) for skill in Skill.query.all()]

    if form.validate_on_submit():
        # Clear existing CharacterSkill entries to avoid duplicates
        CharacterSkill.query.filter_by(character_id=character.id).delete()

        # Add selected skills to the character
        for skill_id in form.skills.data:
            character_skill = CharacterSkill(character_id=character.id, skill_id=skill_id)
            db.session.add(character_skill)

        db.session.commit()

        flash("Skills successfully selected", "success")
        return redirect(url_for("character_overview", character_id=character.id))

    return render_template("choose_skills.html", form=form, character=character)