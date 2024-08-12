# Fallout 2D20 Character Creator

**Video URL:** [Insert your video URL here]

---

## Project Description

The Character Creator is a web-based application designed to assist users in creating new characters for the Fallout 2D20 Tabletop Roleplaying Game. 

The system allows users to create and delete characters, while also providing detailed overviews of each character's attributes, such as basic information, stats, skills, traits, and perks. 

The project is built using Python and Flask, utilizing SQLAlchemy and SQLite for database management, and Jinja2 for rendering dynamic HTML templates.

### Key Features

1. **Character Creation:**
   - Users can create new characters by inputting their name, origin, and other attributes.
   - The dashboard provides a comprehensive view of all characters, enabling users to quickly access or delete characters as needed.

2. **Persistant data:**
   - characters are stored in a relational database, allowing for persistent storage and retrieval.

2. **Detailed Character Overview:**
   - For each character, the system offers a detailed view that breaks down the character's stats, skills, traits, and perks and their derived statistics.

3. **Intuitive User Interface:**
   - The application is designed with simplicity and ease of use in mind. The interface is clean, with clear navigation paths and minimal clutter.
   - Interactive elements are designed with user experience in mind, such as dimming buttons and keeping them inactive until all necessary fields are completed.

4. **Security and Data Integrity:**
   - The system incorporates essential security measures such as Flask-WTF for form handling, CSRF protection, and input validation to ensure that data remains secure and the application is protected from common vulnerabilities.

## Design Considerations

In designing the Character Management System, several key decisions were made to ensure that the application is both functional and scalable:

- **Modular Architecture:**
  - The application is built using a modular architecture, which separates the core logic, database models, and templates into distinct components. This not only improves maintainability but also makes the system more flexible for future expansions or modifications.

- **User-Centric Design:**
  - The design of the application is heavily user-centric. From the dashboard that provides an at-a-glance view of all characters to the detailed character pages, every aspect of the system is designed to be intuitive and accessible. The layout and organization of information are structured to minimize the learning curve and enhance the overall user experience.

- **Scalability:**
  - The use of SQLAlchemy as the ORM layer allows the system to scale efficiently as the number of characters and their associated data grows. This was a critical consideration during development to ensure that the system could handle an increasing amount of data without degrading performance.

- **Template-Driven UI:**
  - The front-end of the application is powered by Jinja2 templates, which enable dynamic rendering of HTML based on the data stored in the database. This approach allows for a seamless integration between the back-end logic and the front-end presentation, ensuring that updates to character data are reflected in real-time.

### Tech Stack
 - Python
    - Flask
    - SQLAlchemy
    - Jinja
    - Werkzeug
    - WTForms
 - SQLite
 - HTML
 - CSS / Boostrap

### Project Structure
```
|   .gitignore
|   config.py
|   readme.md
|   requirements.txt
|   run.py
|   tree.txt
|   
+---app
|   |   forms.py
|   |   models.py
|   |   routes.py
|   |   __init__.py
|   |   
|   +---templates
|          base.html
|          character_overview.html
|          choose_origin.html
|          choose_perks.html
|          choose_skills.html
|          choose_stats.html
|          dashboard.html
|          index.html
|          login.html
|          register.html
|           
+---data
|       perks.csv
|       
+---instance
|       app.db
|       
+---scripts
|       init_db.py
|       populate_attributes.py
|       populate_origins.py
|       populate_perks.py
|       populate_skills.py
|       populate_stats.py
|       populate_traits.py
|       run_population_scripts.py
```

## Installing and Running Web Application
### Cloning the Repository
Follow these steps to clone the repository:

1. **Clone the Repository**: Open your terminal or command prompt and clone the repository to your local machine using the following command:
   ```bash
   git clone https://github.com/Hillgrove/Fallout2D20-Character-Creator.git
   ```

### Installing Required Dependancies
Follow these steps to install the required dependencies (requires Python installed on the system):
1. **Navigate to the Project Directory**: Open your terminal or command prompt and navigate to the directory where the `requirements.txt` file is located: `cd /path/to/your/project`.

2. **(Optional) Create and Activate a Virtual Environment**: It's recommended to create a virtual environment to keep dependencies isolated: `python -m venv venv`. 
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. **Install Dependencies**: Install the dependencies listed in `requirements.txt` using **pip**: `pip install -r requirements.txt`.

After following these steps, all required packages will be installed and your environment will be ready for running the project.

### Initializing Database and Data Populating
1. **Navigate to the Project Directory**: Open your terminal or command prompt and navigate to the directory where `run.py` is located: `cd /path/to/your/project`.
2. **Initialize Database**: Initialize the database by running the following command:
```bash
python.exe .\scripts\init_db.py
```
wait for successful confirmation of database initialization.

3. **Populating Database**: Populate the database by running the following command:
```bash
python.exe .\scripts\run_population_scripts.py
```
wait for successful conformation of database population.

### Running the Web Application
1. **Running Application**: To open the application locally, run the following command:
```bash
python.exe .\run.py
```
2. **Opening the Application**: When running the application it will list which IP and port it runs on. Click on that to open the site in a new window.

Example:

`Running on http://127.0.0.1:5000`

Congratulations! You're now running your own local version of Fallout 2D20 Character Creator.

## Database Design
![Class Diagram](./docs/class%20diagram.png)

The database is intended to be somewhat system agnostic (in terms of TTRPG rules), and it should be able to handle at least a few different rulesets.

### A few of the interesting tables
1. **user**: The table for anything related to your account and access to the application.
2. **character**: The character you've created
3. **origin**: A list of all the various origins / races / backgrounds you can choose (eg. Vault Dweller, Survivor etc). The field `selectable_traits_limit` is used for those origins that can choose from a list of traits an origin can have. 
Some origins have fixed built-in traits, some needs to choose, and others again have both fixed and selectable traits.
4. **trait**: All the various traits an origin can have. It holds all fixed and selectable traits. Special gamerules that breaks normal game logic, is saved in the `trait_data` JSON field. For example, normally all origins only have 1 perk point.
The Survivor is able to choose a trait that gives them 1 more perk point, thus breaking the normal game logic, and the application needs to be aware of this.
The JSON looks like this:
```JSON
{"name": "Extra Perk", "description": "1 more perk", "trait_data": {"extra_perks": 1}, "is_selectable": True}
```
*The backend will look for the __extra_perks__ data and add the number to the total number of perks. This JSON also shows how the selectable traits work in the database.*
5. **origin_trait**: This is a junction table to allows for many-to-many to exist between origins and traits.
6. **character_trait**: This is also a junction table. This is for the those traits that are '"is_selectable": True' and the character has chosen.
7. **stat** and **character_stat**: For the various stats a character can have. In Fallout 2D20 this is the S.P.E.C.I.A.L stats (Strength, Perception, Endurance, Charisma, Intelligence, Agility and Luck)
8. **skill**, **attribute** and **character_skill_attribute**: Tables for the various skills a character can have (eg. Athletics, Lockpick, Sneak etc). Attributes are special 'descriptors' for a skill. In Fallout 2D20 this attribute is called "Tagged". 
The last table is a junction table to bind all together.
9. **perk** and **character_perk**: Various perks a character can have (eg. Armorer. Night Person, Steady Aim etc)




## Backend
### each file:


## Frontend


## Disclaimer

## Conclusion

The Character Management System is a robust, user-friendly application tailored to the needs of RPG and tabletop gaming enthusiasts. It provides a comprehensive platform for managing character profiles, offering detailed insights into each character's attributes and making it easy to maintain and organize multiple characters. The project is built with scalability and maintainability in mind, ensuring that it can grow and adapt to meet the evolving needs of its users. The careful consideration given to user experience, security, and modularity makes this system not only functional but also a joy to use, standing as a valuable tool for any gaming setup.


# MISC
Csrf
Flask login managerDashboard
What will your software do? What features will it have? How will it be executed?
how to install and run yourself