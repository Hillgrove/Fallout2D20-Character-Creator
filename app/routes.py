
from flask import render_template, redirect, request, url_for, flash, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.forms import RegistrationForm, LoginForm, BackgroundForm, StatForm, PerkForm, DeleteForm, DynamicSkillForm
from app.models import User, Character, Stat, CharacterStat, Perk, CharacterPerk, Skill, Origin, CharacterSkillAttribute, Attribute, CharacterTrait, Trait, OriginTrait
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
    # Check if the current user owns the character
    if character.user_id != current_user.id:
        flash("You do not have permission to delete this character", "danger")
        return redirect(url_for("dashboard"))
    
    # Perform the delete operation
    db.session.delete(character)
    try:
        db.session.commit()
        flash("Character successfully deleted", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while deleting the character: {str(e)}", "danger")
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
            new_trait = CharacterTrait(character_id=new_character.id, trait_id=trait_id)
            db.session.add(new_trait)
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
    for origin_trait in origin.origin_traits:
        trait = origin_trait.trait
        if "stat" in trait.trait_data:
            for stat in default_stats:
                if stat["name"] == trait.trait_data["stat"]:
                    stat["max"] = trait.trait_data.get("max", stat["max"])
                    stat["min"] = trait.trait_data.get("min", stat["min"])

    selectable_traits = [
        {"id": trait.trait.id, "name": trait.trait.name, "description": trait.trait.description}
        for trait in origin.origin_traits if trait.trait.is_selectable
    ]
    non_selectable_traits = [
        {"id": trait.trait.id, "name": trait.trait.name, "description": trait.trait.description}
        for trait in origin.origin_traits if not trait.trait.is_selectable
    ]

    response_data = {
        "description": origin.description,
        "selectable_traits": selectable_traits,
        "non_selectable_traits": non_selectable_traits,
        "special_stats": default_stats,
        "selectable_traits_limit": origin.selectable_traits_limit
    }

    return jsonify(response_data)


@app.route("/choose_stats/<int:character_id>", methods=["GET", "POST"])
@login_required
def choose_stats(character_id):
    character = Character.query.get_or_404(character_id)
    form = StatForm(origin_id=character.origin_id)
    
    # Fetch the character's selected traits
    selected_traits = [trait.trait for trait in character.character_traits]
    carry_weight_trait = next((trait for trait in selected_traits if 'carry_weight' in trait.trait_data), None)
    
    carry_weight_base = 150
    extra_special_points = 0
    if carry_weight_trait:
        carry_weight_base = carry_weight_trait.trait_data['carry_weight']
    
    extra_special_points_trait = next((trait for trait in selected_traits if 'extra_special_points' in trait.trait_data), None)
    if extra_special_points_trait:
        extra_special_points = extra_special_points_trait.trait_data['extra_special_points']

    if form.validate_on_submit():
        try:
            CharacterStat.query.filter_by(character_id=character.id).delete()
            stats = {stat_name: getattr(form, stat_name.lower()).data for stat_name in ["Strength", "Perception", "Endurance", "Charisma", "Intelligence", "Agility", "Luck"]}
            if sum(stats.values()) > character.starting_stat_points + extra_special_points:
                flash("You have exceeded the allowed stat points.", "danger")
            else:
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

    return render_template("choose_stats.html", form=form, character=character, stats=Stat.query.all(), carry_weight_base=carry_weight_base, carry_weight_trait=carry_weight_trait is not None, extra_special_points=extra_special_points)


@app.route("/choose_perks/<int:character_id>", methods=["GET", "POST"])
@login_required
def choose_perks(character_id):
    character = Character.query.get_or_404(character_id)
    form = PerkForm()

    # Calculate extra perks allowed
    extra_perks = 0
    traits = {trait.trait_id: trait.trait for trait in character.character_traits}
    extra_perks_trait = next((trait for trait in traits.values() if 'extra_perks' in trait.trait_data), None)
    if extra_perks_trait:
        extra_perks = extra_perks_trait.trait_data['extra_perks']

    allowed_perks = 1 + extra_perks

    if form.validate_on_submit():
        selected_perks = request.form.getlist("perks")
        if len(selected_perks) > allowed_perks:
            flash(f"You can only select up to {allowed_perks} perks.", "danger")
        else:
            for perk_id in selected_perks:
                character_perk = CharacterPerk(
                    character_id=character.id,
                    perk_id=perk_id
                )
                db.session.add(character_perk)
            db.session.commit()
            return redirect(url_for("choose_skills", character_id=character.id))

    perks = [perk for perk in Perk.query.all() if meets_stat_requirements(character, perk)]
    
    return render_template("choose_perks.html", form=form, character=character, perks=perks, allowed_perks=allowed_perks)


@app.route('/choose_skills/<int:character_id>', methods=['GET', 'POST'])
def choose_skills(character_id):
    skills = Skill.query.all()
    tagged_attribute = Attribute.query.filter_by(name='Tagged').first()
    character = Character.query.get_or_404(character_id)
    origin = character.origin

    # Default total points
    intelligence_stat = CharacterStat.query.filter_by(character_id=character_id, stat_id=Stat.query.filter_by(name="Intelligence").first().id).first()
    intelligence_value = intelligence_stat.value if intelligence_stat else 0
    total_points = 9 + intelligence_value

    # Extra tag skills from traits
    extra_tag_skills = 0
    free_tag_skills = []

    # Check traits chosen by the character
    character_traits = {ct.trait_id: ct.trait for ct in character.character_traits}

    # Process origin traits (non-selectable traits)
    for origin_trait in origin.origin_traits:
        trait = origin_trait.trait
        trait_data = trait.trait_data
        if "extra_tag_skills" in trait_data and not trait.is_selectable:
            extra_tag_skills += trait_data["extra_tag_skills"]
        if "tag" in trait_data and not trait.is_selectable:
            free_tag_skills.append(trait_data["tag"])

    # Process selectable traits
    for trait_id, trait in character_traits.items():
        trait_data = trait.trait_data
        if "extra_tag_skills" in trait_data and trait.is_selectable:
            extra_tag_skills += trait_data["extra_tag_skills"]
        if "tag" in trait_data and trait.is_selectable:
            free_tag_skills.append(trait_data["tag"])

    max_tags = 3 + extra_tag_skills

    SkillForm = DynamicSkillForm(skills)

    # Retrieve existing values from the database
    existing_values = {
        skill.id: CharacterSkillAttribute.query.filter_by(character_id=character_id, skill_id=skill.id).first()
        for skill in skills
    }

    form = SkillForm()

    # Pre-populate form with existing values
    if request.method == 'GET':
        for skill in skills:
            skill_field_name = f'skill_{skill.id}'
            tagged_field_name = f'tagged_{skill.id}'
            existing_value = existing_values[skill.id]
            if existing_value:
                form[skill_field_name].data = existing_value.value
                form[tagged_field_name].data = existing_value.attribute_id == tagged_attribute.id
            if skill.name in free_tag_skills:
                form[tagged_field_name].data = True

    if form.validate_on_submit():
        tagged_count = sum(1 for skill in skills if getattr(form, f'tagged_{skill.id}').data and skill.name not in free_tag_skills)

        if tagged_count > max_tags:
            flash(f'You can only select up to {max_tags} tags.', 'error')
        else:
            spent_points = sum(getattr(form, f'skill_{skill.id}').data or 0 for skill in skills)

            if spent_points > total_points:
                flash('You have exceeded the allowed skill points.', 'error')
            else:
                for skill in skills:
                    skill_field_name = f'skill_{skill.id}'
                    tagged_field_name = f'tagged_{skill.id}'
                    skill_value = getattr(form, skill_field_name).data or 0  # Default to 0 if empty
                    is_tagged = getattr(form, tagged_field_name).data
                    character_skill_attr = CharacterSkillAttribute.query.filter_by(character_id=character_id, skill_id=skill.id).first()
                    if character_skill_attr:
                        character_skill_attr.value = skill_value
                        if is_tagged:
                            character_skill_attr.attribute_id = tagged_attribute.id
                        else:
                            if character_skill_attr.attribute_id == tagged_attribute.id:
                                character_skill_attr.attribute_id = None
                    else:
                        new_skill_attr = CharacterSkillAttribute(character_id=character_id, skill_id=skill.id, value=skill_value)
                        if is_tagged:
                            new_skill_attr.attribute_id = tagged_attribute.id
                        db.session.add(new_skill_attr)
                db.session.commit()
                return redirect(url_for('character_overview', character_id=character_id))

    return render_template('choose_skills.html', form=form, skills=skills, character_id=character_id, total_points=total_points, max_tags=max_tags, free_tag_skills=free_tag_skills)


@app.route("/character_overview/<int:character_id>")
@login_required
def character_overview(character_id):
    character = Character.query.get_or_404(character_id)

    # Fetch the manually selected traits (including non-selectable)
    character_traits = db.session.query(Trait).join(CharacterTrait).filter(
        CharacterTrait.character_id == character.id).all()

    # Fetch the traits associated with the character's origin (non-selectable)
    origin_traits = db.session.query(Trait).join(OriginTrait).filter(
        OriginTrait.origin_id == character.origin_id).all()

    # Combine both sets of traits, ensuring no duplicates
    all_traits = {trait.id: trait for trait in character_traits}  # Use a dictionary to prevent duplicates
    for origin_trait in origin_traits:
        if origin_trait.id not in all_traits:
            all_traits[origin_trait.id] = origin_trait

    # Filter the all_traits to only include non-selectable traits and chosen selectable traits
    final_traits = [trait for trait in all_traits.values() if not trait.is_selectable or trait in character_traits]

    # Fetch other necessary data
    character_stats = CharacterStat.query.filter_by(character_id=character.id).all()
    character_skill_attributes = CharacterSkillAttribute.query.filter_by(character_id=character.id).all()
    character_perks = CharacterPerk.query.filter_by(character_id=character.id).all()

    # Initialize a set to track tagged skills
    tagged_skills = set()

    # Add manually tagged skills
    for skill_attr in character_skill_attributes:
        if skill_attr.attribute_id:  # Assuming attribute_id indicates the skill is tagged
            tagged_skills.add(skill_attr.skill.name)

    # Add free tagged skills from traits
    for trait in final_traits:
        if 'tag' in trait.trait_data:
            tagged_skills.add(trait.trait_data['tag'])

    # Update the character skills with tagging information
    for skill_attr in character_skill_attributes:
        skill_attr.is_tagged = skill_attr.skill.name in tagged_skills

    return render_template("character_overview.html",
                            character=character, 
                            character_stats=character_stats, 
                            character_skill_attributes=character_skill_attributes, 
                            character_perks=character_perks, 
                            character_traits=final_traits)


# Helper Functions
def meets_stat_requirements(character, perk):
    character_stats = {stat.stat.name: stat.value for stat in character.character_stats}
    if perk.stat_1 and character_stats.get(perk.stat_1.name, 0) < perk.amount_1:
        return False
    if perk.stat_2 and character_stats.get(perk.stat_2.name, 0) < perk.amount_2:
        return False
    return True
