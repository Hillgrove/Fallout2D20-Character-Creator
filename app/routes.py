
from flask import render_template, redirect, request, url_for, flash, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.forms import RegistrationForm, LoginForm, BackgroundForm, StatForm, PerkForm, DeleteForm, SkillForm
from app.models import User, Character, Stat, CharacterStat, Perk, CharacterPerk, Skill, Origin, OriginTrait, CharacterSkillAttribute, Attribute
from werkzeug.security import generate_password_hash, check_password_hash
import logging

logging.basicConfig(level=logging.INFO)

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
    if character.user_id != current_user.id:
        flash("You do not have permission to delete this character", "danger")
        return redirect(url_for("dashboard"))
    db.session.delete(character)
    db.session.commit()
    flash("Character successfully deleted", "success")
    return redirect(url_for("dashboard"))


@app.route("/choose_origin", methods=["GET", "POST"])
@login_required
def choose_origin():
    form = BackgroundForm(origin_id=request.form.get('origin_id', type=int, default=-1))
    if form.validate_on_submit():
        new_character = Character(
            name=form.name.data,
            origin_id=form.origin_id.data,
            user_id=current_user.id
        )
        db.session.add(new_character)
        db.session.commit()

        selected_traits = form.selectable_traits.data
        for trait_id in selected_traits:
            origin_trait = OriginTrait.query.filter_by(origin_id=form.origin_id.data, trait_id=trait_id).first()
            if origin_trait:
                new_character.origin.origin_traits.append(origin_trait)  # Access through the origin relationship
        db.session.commit()

        return redirect(url_for("choose_stats", character_id=new_character.id))
    return render_template("choose_origin.html", form=form)


@app.route("/get_origin_description")
@login_required
def get_origin_description():
    origin_id = request.args.get('origin_id', type=int)
    origin = Origin.query.get_or_404(origin_id)

    # Fetch all default stats from the Stat table
    default_stats = [{"name": stat.name, "min": 4, "max": 10} for stat in Stat.query.all()]

    # Adjust stats based on origin traits
    for trait in origin.origin_traits:
        if "stat" in trait.trait.trait_data:
            for stat in default_stats:
                if stat["name"] == trait.trait.trait_data["stat"]:
                    stat["max"] = trait.trait.trait_data.get("max", stat["max"])
                    stat["min"] = trait.trait.trait_data.get("min", stat["min"])

    selectable_traits = [{"id": trait.trait.id, "name": trait.trait.name} for trait in origin.origin_traits if trait.trait.is_selectable]

    return jsonify(description=origin.description, selectable_traits=selectable_traits, special_stats=default_stats)


@app.route("/choose_stats/<int:character_id>", methods=["GET", "POST"])
@login_required
def choose_stats(character_id):
    character = Character.query.get_or_404(character_id)
    form = StatForm(origin_id=character.origin_id)
    if form.validate_on_submit():
        try:
            CharacterStat.query.filter_by(character_id=character.id).delete()
            stats = {stat_name: getattr(form, stat_name.lower()).data for stat_name in ["Strength", "Perception", "Endurance", "Charisma", "Intelligence", "Agility", "Luck"]}
            if sum(stats.values()) > character.starting_stat_points:
                flash("You have exceeded the allowed stat points.", "danger")
                return render_template("choose_stats.html", form=form, character=character, stats=Stat.query.all())

            for stat_name, stat_value in stats.items():
                stat = Stat.query.filter_by(name=stat_name).first()
                if stat:
                    character_stat = CharacterStat(character_id=character.id, stat_id=stat.id, value=stat_value)
                    db.session.add(character_stat)

            db.session.commit()
            return redirect(url_for("choose_perks", character_id=character.id))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving stats: {e}")
            flash("An error occurred while saving your stats. Please try again.", "danger")
    return render_template("choose_stats.html", form=form, character=character, stats=Stat.query.all())


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
    skills = Skill.query.all()
    form = SkillForm()

    if request.method == 'GET':
        # Populate the form with a field for each skill with default values
        form.skills.entries = []
        for skill in skills:
            form.skills.append_entry({'ranks': 0, 'tagged': False})

    if form.validate_on_submit():
        # Process form data
        for i, skill_form in enumerate(form.skills.entries):
            skill = skills[i]
            ranks = skill_form.ranks.data
            tagged = skill_form.tagged.data
            attribute = Attribute.query.filter_by(name='Tagged').first()
            
            character_skill_attribute = CharacterSkillAttribute(
                character_id=character.id,
                skill_id=skill.id,
                attribute_id=attribute.id if tagged else None,
                value=ranks
            )
            db.session.merge(character_skill_attribute)
        db.session.commit()
        flash("Skills successfully selected", "success")
        return redirect(url_for("character_overview", character_id=character.id))
    else:
        if request.method == 'POST':
            print("Form validation failed")
            print(request.form)  # Debugging line to print the form data received
            print("Form Errors:", form.errors)
            for i, skill_form in enumerate(form.skills.entries):
                print(f"Skill {i}: ranks={skill_form.ranks.data}, tagged={skill_form.tagged.data}")
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    print(f"Field: {fieldName} - Error: {err}")

    return render_template("choose_skills.html", form=form, character=character, skills=skills, zip=zip)













@app.route("/character_overview/<int:character_id>")
@login_required
def character_overview(character_id):
    character = Character.query.get_or_404(character_id)

    character_stats = CharacterStat.query.filter_by(character_id=character.id).all()
    character_skill_attributes = CharacterSkillAttribute.query.filter_by(character_id=character.id).all()
    character_perks = CharacterPerk.query.filter_by(character_id=character.id).all()

    return render_template("character_overview.html", character=character, character_stats=character_stats, character_skill_attributes=character_skill_attributes, character_perks=character_perks)
