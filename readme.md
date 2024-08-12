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
## Database Design
![Class Diagram](./class%20diagram.png)

## Backend
### each file:


## Frontend


## Disclaimer

## Conclusion

The Character Management System is a robust, user-friendly application tailored to the needs of RPG and tabletop gaming enthusiasts. It provides a comprehensive platform for managing character profiles, offering detailed insights into each character's attributes and making it easy to maintain and organize multiple characters. The project is built with scalability and maintainability in mind, ensuring that it can grow and adapt to meet the evolving needs of its users. The careful consideration given to user experience, security, and modularity makes this system not only functional but also a joy to use, standing as a valuable tool for any gaming setup.
