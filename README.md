# Fallout 2D20 Character Creator

**Video URL**: [:https://www.youtube.com/watch?v=gcVHocFL4qA](https://www.youtube.com/watch?v=gcVHocFL4qA)

---

## Project Description

The Character Creator is a web-based application designed to assist users in creating new characters for the Fallout 2D20 Tabletop Roleplaying Game. 

The system allows users to create and delete characters, while also providing detailed overviews of each character's attributes, such as basic information, stats, skills, traits, and perks. 

The project is built using Python and Flask. It uses SQLAlchemy for ORM and SQLite for database management. Jinja is employed for rendering dynamic HTML templates.

### Key Features

1. **Character Creation:**
   - Users can create new characters by inputting their name, origin, and other attributes.
   - The dashboard provides a comprehensive view of all characters, enabling users to quickly access or delete characters as needed.

2. **Persistent Data:**
   - Character data is stored persistently in a relational database, ensuring that user data remains consistent and retrievable across sessions.

2. **Detailed Character Overview:**
   - For each character, the system offers a detailed view that breaks down the character's stats, skills, traits, and perks and their derived statistics.

3. **Intuitive User Interface:**
   - The application is designed with simplicity and ease of use in mind. The interface is clean, with clear navigation paths and minimal clutter.
   - Interactive elements are designed with user experience in mind, such as disabling buttons and keeping them inactive until all necessary fields are completed.

4. **Security and Data Integrity:**
   - The system incorporates essential security measures such as Flask-WTF for form handling, CSRF protection, and input validation to ensure that data remains secure and the application is protected from common vulnerabilities. CSRF protection helps prevent cross-site request forgery attacks by ensuring that form submissions come from trusted sources.

### Tech Stack
 - Python
    - Flask
    - SQLAlchemy
    - Jinja
    - Werkzeug
    - WTForms
 - JavaScript
 - SQLite
 - HTML
 - CSS (Bootstrap)

<br><br>

# Installing and Running Web Application
## Cloning the Repository
Follow these steps to clone the repository:

1. **Clone the Repository**: Open your terminal or command prompt and clone the repository to your local machine using the following command:
   ```bash
   git clone https://github.com/Hillgrove/Fallout2D20-Character-Creator.git
   ```

## Installing Required Dependencies
Follow these steps to install the required dependencies (requires Python installed on the system):
1. **Navigate to the Project Directory**: Open your terminal or command prompt and navigate to the directory where the `requirements.txt` file is located: `cd /path/to/your/project`.

2. **(Optional) Create and Activate a Virtual Environment**: It's recommended to create a virtual environment to keep dependencies isolated: `python -m venv venv`. 
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. **Install Dependencies**: Install the dependencies listed in `requirements.txt` using **pip**: `pip install -r requirements.txt`.

After following these steps, all required packages will be installed and your environment will be ready for running the project.

## Initializing Database and Data Populating
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

## Running the Web Application
1. **Running Application**: To open the application locally, run the following command:
```bash
python.exe .\run.py
```
2. **Opening the Application**: When running the application it will list which IP and port it runs on. Click on that to open the site in a new window.

Example:

`Running on http://127.0.0.1:5000`

Congratulations! You're now running your own local version of the **Fallout 2D20 Character Creator**.

<br><br>

# Database Design
![Class Diagram](./docs/class%20diagram.png)

The database is intended to be somewhat system agnostic (in terms of TTRPG rules), and it should be able to handle at least a few different rulesets.

## A quick overview of the different tables
- **user**: The table for anything related to your account and access to the application.
- **character**: The character you've created
- **origin**: A list of all the various origins / races / backgrounds you can choose (eg. Vault Dweller, Survivor etc). The field `selectable_traits_limit` is used for those origins that can choose from a list of traits an origin can have. 
Some origins have fixed built-in traits, some needs to choose, and others again have both fixed and selectable traits.
- **trait**: All the various traits an origin can have. It holds all fixed and selectable traits. Special gamerules that breaks normal game logic, is saved in the `trait_data` JSON field. For example, normally all origins only have 1 perk point.
The Survivor is able to choose a trait that gives them 1 more perk point, thus breaking the normal game logic, and the application needs to be aware of this.
The JSON looks like this:
```JSON
{"name": "Extra Perk", "description": "1 more perk", "trait_data": {"extra_perks": 1}, "is_selectable": True}
```
*The backend will look for the __extra_perks__ data and add the number to the total number of perks. This JSON also shows how the selectable traits work in the database.*

- **origin_trait**: This is a junction table to allows for many-to-many to exist between origins and traits.
- **character_trait**: This is also a junction table. This is for the those traits that are '"is_selectable": True' and the character has chosen.
- **stat** and **character_stat**: For the various stats a character can have. In Fallout 2D20 this is the S.P.E.C.I.A.L stats (Strength, Perception, Endurance, Charisma, Intelligence, Agility and Luck)
- **skill**, **attribute** and **character_skill_attribute**: Tables for the various skills a character can have (eg. Athletics, Lockpick, Sneak etc). Attributes are special 'descriptors' for a skill. In Fallout 2D20 this attribute is called "Tagged". 
The last table is a junction table to bind all together.
- **perk** and **character_perk**: Various perks a character can have (eg. Armorer. Night Person, Steady Aim etc)

<br><br>

# Files
## Project Structure
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
|       attributes.csv
|       origins.csv
|       perks.csv
|       skills.csv
|       stats.csv
|       traits.csv
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

## File Overview
### Data Files
- **Data CSV files**: Store essential data used in the character creation process. Each CSV file provides structured data that is used to populate the respective sections in the character creator.
- **app.db**: SQLite database file taht stores persistent data for the web application, such as user-generated characters and any other data that needs to be retained across sessions. It acts as the main storage system for the app, enabling data retrieval and manipulation through SQL queries.
- **init_db.py**: This script sets up the system path, initializes the Flask app, and creates the database schema. It logs the success or failure of the initialization process and is designed to be run as a standalone script to set up the database for the application.
- **Population scripts**: These scripts are responsible for initializing the database and populating it with predefined data. They set up the essential data that the application requires for the character creation process.
- **run_population_scripts.py**: This script sequentially executes a series of population scripts that populate the database with predefined data. It uses subprocess to run each script and logs the success or failure of each execution, ensuring that the scripts are run in the correct order and the data is properly initialized.

### Backend Files
- **models.py**: This file defines the database models and relationships for the application's data structure. It uses SQLAlchemy to represent entities, manage relationships between them, and enforce constraints like cascading deletes and unique combinations of fields. These models serve as the foundation for the application's data management and interactions.
- **forms.py**: Defines various forms used in the application, leveraging Flask-WTF and WTForms to manage user input and validation.
- **routes.py**: Manages the application's URL routing and handles user interactions, including data processing and form submissions. It coordinates the application's flow and interactions, ensuring users are directed to the correct pages and that their inputs are handled appropriately.
- **config.py**: This file defines configuration settings for the application, including secret keys and database URI. It allows for environment-based configuration with fallback default values.
- **__init__.py**: Initializes the Flask application, configures extensions like SQLAlchemy, Flask-Login, and CSRF protection, and imports routes to register them with the app.
- **run.py**: This file serves as the entry point for running the Flask application, launching it in debug mode. allowing for live code reloading and detailed error messages.


### Frontend Files
- **base.html**: Provides the base HTML template for the web application, including a responsive layout with a Bootstrap navbar and dynamic content blocks. It also includes space for flashing messages and integrates essential JavaScript libraries for functionality.
- **character_overview.html**: A detailed character overview page.
- **choose_origin.html**: An origin selection page.
- **choose_perks.html**: A perks selection page.
- **choose_skills.html**: A skills selection page.
- **choose_stats.html**: A stats selection page.
- **dashboard.html**: A dashboard for managing characters.
- **index.html**: Homepage for the Fallout 2D20 Character Creator
- **login.html**: Login page.
- **register.html**: Registration page.

### Misc files
- **requirements.txt**: Specifies the exact versions of Python packages needed for the project.
- **readme.md**: Provides an overview of the project, including its purpose, features, and installation instructions

<br><br>

# Disclaimer
Due to limited prior experience with JavaScript, a significant portion of the JavaScript used in this application was generated by AI and manually adjusted as needed.

<br><br>

# Conclusion
The Character Creation System is a streamlined, web-based tool designed to simplify and accelerate the process of creating new characters for Fallout 2D20 TTRPG. The application offers a modern, responsive interface that enhances usability across various devices, though optimal use is recommended on medium to large screen devices.

One of the project's standout features is its web-based nature, which contrasts with the more common spreadsheet solutions, offering users a more interactive and accessible experience. Despite its simplicity, the project provided a valuable learning experience, allowing for the re-discovery of Python and the exploration of new tools like SQLAlchemy and Flask.

The most rewarding aspect of the project was successfully integrating the backend with the frontend, despite the challenges involved. This project, as the final requirement for the CS50x course, represents a significant step in improving backend development skills while recognizing the importance of a polished user interface. Although the project highlighted the need for further focus on frontend skills, it has been a crucial learning experience, especially in understanding the value of unit testing and the role of client-side technologies like JavaScript.
