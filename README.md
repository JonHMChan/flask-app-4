# Flask App 4: Database Design, Postgres, and SQL
For this exercise, you'll be writing the database setup and queries that power a fully built front end. The application is also live at https://shrouded-temple-59174.herokuapp.com/ if you would like to see how it works.

![Pokedex Homepage](https://raw.githubusercontent.com/JonHMChan/flask-app-3/master/static/img/preview.png)

## What you'll practice
 - Database Design
 - Postgres
 - SQL
 - Psycopg2
 - Flask
 - Jinja
 - AJAX
 - API calls
 - Command Line
 - Git
 - GitHub

 ## Files and folders

 **For you**
 - `/data` - Contains the `database.json` file you will import into your Postgres database, a `db.py` file you will use for your database connection and setup, and a `schema.sql` command that will set up your tables when you run `localhost:5000/migrate`.
 - `.env` - You will need to create a `.env` file at the root of this application containing the database URL for your Postgres database. For example, on my computer, `.env` would contain `DATABASE_URL=postgres://postgres:postgres@localhost:5432/pokedex`
 - `app.py` - Contains the `/migrate` path which when run, will set up your database and import `database.json` into your tables. You will need to write the code that powers this route.
 - `pokemon.py` - Contains all of the `GET` methods for the Pokemon API. You will also need to support search functionality in `/api/pokemon`
 - `teams.py` - Contains all of the API routes for Teams. You will need to implement all of the REST operations using the database.

 **Do not touch**
 - `README.md` - The instructions you're reading right now.
 - `setup.sh` - The file that will set your application up for you. See the "Setup" instructions below.
 - `requirements.txt` - A file that stores all of your Python dependencies (e.g. Flask) so when you run `pip install -r requirements.txt`, you'll download all the dependencies you need. For more information, see "How setup.sh works"
 - `.gitignore` - A file that tells `git` which files to ignore when you use version control.
 - `/venv` - A folder that contains all of your virtual environment files and downloaded dependencies from `pip`. For more information, see "How setup.sh works"
 - `/__pycache__` - You'll probably have this folder generated. It is something created by Python 3 when you run it, and you can safely ignore it.

# Setup
These instructions are a simplified version of the Flask [installation instructions](https://flask.palletsprojects.com/en/1.1.x/installation/) and [quickstart](https://flask.palletsprojects.com/en/1.1.x/quickstart/). If you have any questions, feel free to reach out to me.

1. Clone this repository using `git clone` and `cd` from your command line into the repository folder.
2. Make sure you have Python 3 installed. You can check this by seeing if the command `python3` works in your command line. If you successfully run `python3`, you can exit the interpreter by typing `quit()` then hitting Enter. If you don't have Python 3 installed, follow [these instructions](https://realpython.com/installing-python/).
3. **NEW** Download Postgres.app. This will install the Postgres database on your computer. This should create a Postgres icon (a small elephant in the top right toolbar of your Mac). If you click on this icon, it will have an option to "Open Postgres" and you can start and stop your database using these buttons.
4. **NEW** After installing Postgres, you need to make the `psql` command in your Terminal works in order for the Python Postgres driver `psycopg2` to be properly installed. This means you will need to change your `.bash_profile` file located in your home directory (`~`) (the directory you first land on when you open a new Terminal window) and add an `EXPORT` line.
  - Open up the `.bash_profile` file by using `code ~/.bash_profile` to open it in Visual Studio Code. If `code` doesn't work, you can install it following [these instructions](https://code.visualstudio.com/docs/setup/mac).
  - Once opened, you want to add a line at the bottom of the file with the following: `export PATH="/Applications/Postgres.app/Contents/Versions/9.6/bin:$PATH"`. The value for `PATH` might be different for you depending on the version of Postgres.app you downloaded.
  - Save your `.bash_profile` changes, restart the Terminal, and try running the command `psql`. This should open up the Command Line interface for Postgres, and it means it was properly installed for you to use `sh setup.sh`.
5. From the root of the repository, run the following command: `sh setup.sh`. This is a file I've written to automate the initial setup of this application. It will start your app automatically, and you can go to `localhost:5000` in a web browser to view it. If you want detailed instructions on how this file works, go to "How setup.sh works" below.
6. Whenever you're about to work on your application, make sure to run `. venv/bin/activate` first to start your virtual environment, then you can run `flask run` from the root of your repository to start your application.
 - To stop your server it's running in the command line, hit `Control + C` to stop the server.
 - If you change your HTML files, you'll have to restart the server to see changes.


## How setup.sh works
1. Python 3 comes with venv, a "virtual environment" to manage packages like `Flask` that you'll need to run your application. When you first clone this repository, run `python3 -m venv venv` from the root of the repository to create a virtual environment for your application. This will create a few folders and files related to venv, in a `venv` folder.
2. Once you've set up a virtual environment, whenever you're about to work on your app, make sure to run `. venv/bin/activate` from the root of the repository. You should then see `(venv)` prefixed in your command line to show that you're using the virtual environment. After you do this, you should be able to download packages and run your application.
3. Once you are using the virtual environment, make sure you install all the dependencies for this application by running `pip install -r requirements.txt` (if you're using Python 3, you might need to use `pip3` instead of `pip`. You only need to do this once and don't need to again when you want to run your application.
4. Once you have `Flask` properly installed, make sure you set your environment variables so Flask knows what file to start with. In this repository, the app starts with the file `app.py`. If you rename `app.py` or want to use a different file as the entrypoint, you'll have to run `export FLASK_APP={FILENAME}` and replace `{FILENAME}` with the correct filename to make sure the app runs.
5. Once you have everything setup, you should be able to run `flask run` and your server should start listening. Go to a browser at `localhost:5000` and you should see your app running.

# Requirements
You'll be focusing database setup, data migration, and queries that power an existing Pokemon front end. This will require intimate knowledge of database design, Postgres, and SQL. In addition to the requirements below, you can see the full solution of this application running at https://shrouded-temple-59174.herokuapp.com/.

1. **Set Up Postgres** - You'll need to install Postgres and psycopg2 and set up environment variables to get your database connection going before you do anything else.
 - Follow the new setup instructions with Postgres additions to set up a local database.
 - Make sure `psql` is working in your command line.
 - `db.py` is where your Postgres connection is established and should connect to your local database properly.
 - Add your environment variables for connecting to the database in a new `.env` file at the root of your application.
2. **Database Migration** (`localhost:5000/migrate`) - You'll need to set up your database tables when a user hits this route.
 - Change `schema.sql` so it sets up all of your database tables using the database connection in `db.py`
 - `schema.sql` should be idempotent. Research what that means.
 - You should read the contents of `database.json` and import all of the data in that file into your Postgres tables.
 - Your database tables should follow best practices of setting up relationships between objects like Pokemon, teams, types, and evolutions.
 - If you implement your migrations successfully, you should be able to stop your server, start it again, and all of your database changes should remain
3. **API with SQL** (`localhost:5000/api`) - You need to reimplement all of the Pokemon and team APIs using SQL instead of `database.json`. Study the front end code to understand how your API should work.
 - The Pokemon API should use database calls to power its `GET` routes.
 - The Pokemon API should implement basic search, e.g. `localhost:5000/api/pokemon?search=p` should find Pokemone that start with the letter `p`.
 - The Teams API should implement a full REST pattern using SQL.

## What you need to know
 To properly complete this exercise, you'll need to understand a few concepts in a number of different technologies:

Postgres:

 - How to set up a Postgres database, start it, and stop it. Use Postgres.app to simplify this and follow the new setup instructions.
 - What environment variables are, how to use them in Python (`os` package), and using `.env` to set environment variables.
 - How to setup `psql` in the command line. Look at the new instructions for clarity.
 - How to set up new databases, login, and execute commands using `psql`.
 - How Postgres connection URLs work and how they can be used with `.env` to connect to your database.
 - How to use an app like Postico to visualize your Postgres databases.

Database Design:

 - How to write code in a `.sql` file to create a database schema (like `schema.sql`). Essentially, you need to know how to create and alter a database so you can set up your tables for the first time.
 - What it means for code to be idempotent, and why your schema setup code (like `schema.sql`) should be idempotent.
 - How to create different tables to represent your objects. In this case, you want to write tables to represent Pokemon, Teams, and their relationships. You may also have to create new tables for other properties like types, evolutions, and team members.
 - How to set up relationships between different tables, especially if they are one-to-many relationships or many-to-many relationships. Look up foreign keys and ACID.
 - What data types are appropriate for each piece of data (e.g. `TEXT`, `INTEGER`, etc.)
 - What a `PRIMARY KEY` is and how it's used to automatically increment and set an ID

psycopg2:

 - What psycopg2 is and how it connects Python and Postgres together.
 - How `psycopg2.connect()` works to establish a connection to your database.
 - What a cursor is and how `connection.cursor()` is used, especially if it can be reused.
 - How to execute SQL queries using `cursor.execute()` with parameters.
 - How to use `connection.commit()` to commit database transactions.
 - How to use `cursor.fetchone()` and `cursor.fetchall()`.
 - How to translate SQL query values into dictionaries in Python.

SQL:
 - Using `SELECT`, `UPDATE`, `INSERT`, and `DELETE`.
 - How to use SQL to set up a REST API.
 - Using `WHERE` to limit execution of SQL queries.
 - How to do basic joins with `JOIN` on two tables or more.
 - How to use `LIKE` or `ILIKE` for searching.
 - How to use `IN` to specify several conditions in a `WHERE` clause.
