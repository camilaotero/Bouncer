# This project was created by Camila and Tetsu, equally sharing the work done.
# We referred to PSet9 of CS50 "Finance" when implementing the structure of the website, layout baseline, session implementations, hash generation
import os
import requests
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, hostlogin_required, partyerlogin_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 library to use SQLite database
db = SQL("sqlite:///bouncer.db")

@app.after_request
def after_request(response):
    #"""Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Initial page that shows when user reaches link, or when user logs out; renders index template
@app.route("/")
def index():
    return render_template("index.html")

# Login page for hosts   
@app.route("/hostlogin", methods=["GET", "POST"])
def hostlogin():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM hostusers WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password")

        # Remember which user has logged in
        session["hostusers_id"] = rows[0]["id"]

        # Redirect user to host home page
        return redirect("/hosthome")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("hostlogin.html")


# Login page for partyers  
@app.route("/partyerlogin", methods=["GET", "POST"])
def partyerlogin():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM partyerusers WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password")

        # Remember which user has logged in
        session["partyerusers_id"] = rows[0]["id"]

        # Redirect user to partyer home page
        return redirect("/partyerhome")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("partyerlogin.html")


# Function that logs out users when they click the "log out" button
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to main index form
    return redirect("/")


# Registers host users
@app.route("/hostregister", methods=["GET", "POST"])
def hostregister():
    """Register user"""
    if request.method == "POST":

        # Defining special symbols & variable for user, pass, & confirmation inputted by user
        special_symbol = ['$', '@', '#', '%', '!', '*', '&', '^']
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate username
        if not username:
            return apology("Missing username")

        # Check if username already exists
        username_check = db.execute("SELECT username FROM hostusers WHERE username=?", username)
        for i in username_check:
            if username == i["username"]:
                return apology("Username already exists")

        # Validate email
        if not email:
            return apology("Missing email")

        # Validate password
        if not password:
            return apology("Missing password")

        # (Personal touch) Ensure password is a certain length
        if len(password) < 6:
            return apology("Length should be at least 6 characters")

        # Ensure password contains at least one number
        if not any(char.isdigit() for char in password):
            return apology("Password should have at least one number")

        # Ensure password has at least one uppercase letter
        if not any(char.isupper() for char in password):
            return apology("Password should have at least one uppercase letter")

        # Ensure password has at least one lowercase letter
        if not any(char.islower() for char in password):
            return apology("Password should have at least one lowercase letter")

        # Ensure password has at least one special symbol
        if not any(char in special_symbol for char in password):
                return apology("Password should have at least one symbol $@#%!*&^")

        # Check if confirmation matches initial password entered
        if confirmation != password:
            return apology("Passwords do not match")

        # Hash password
        hashed_pass = generate_password_hash(password)

        # Insert data into database
        db.execute("INSERT INTO hostusers (username, hash, email) VALUES(?, ?, ?)", username, hashed_pass, email)

        # Go back to homepage
        return redirect("/hosthome")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("hostregister.html")


# Registers partyer users
@app.route("/partyerregister", methods=["GET", "POST"])
def partyerregister():
    """Register user"""
    if request.method == "POST":

        # Defining special symbols & variable for user, pass, & confirmation inputted by user
        special_symbol = ['$', '@', '#', '%', '!', '*', '&', '^']
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate username
        if not username:
            return apology("Missing username")

        # Check if username already exists
        username_check = db.execute("SELECT username FROM partyerusers WHERE username=?", username)
        for i in username_check:
            if username == i["username"]:
                return apology("Username already exists")

        # Validate email
        if not email:
            return apology("Missing email")

        # Validate password
        if not password:
                return apology("Missing password")

        # (Personal touch) Ensure password is a certain length
        if len(password) < 6:
            return apology("Length should be at least 6 characters")

        # Ensure password contains at least one number
        if not any(char.isdigit() for char in password):
            return apology("Password should have at least one number")

        # Ensure password has at least one uppercase letter
        if not any(char.isupper() for char in password):
            return apology("Password should have at least one uppercase letter")

        # Ensure password has at least one lowercase letter
        if not any(char.islower() for char in password):
            return apology("Password should have at least one lowercase letter")

        # Ensure password has at least one special symbol
        if not any(char in special_symbol for char in password):
            return apology("Password should have at least one symbol $@#%!*&^")

        # Check if confirmation matches initial password
        if confirmation != password:
            return apology("Passwords do not match")

        # Hash password
        hashed_pass = generate_password_hash(password)

        # Insert data into database
        db.execute("INSERT INTO partyerusers (username, hash, email) VALUES(?, ?, ?)", username, hashed_pass, email)

        # Go back to homepage
        return redirect("/partyerhome")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("partyerregister.html")


# Host home page: list out parties planned and their info
@app.route("/hosthome", methods=["GET"])
@hostlogin_required
def hosthome():
    # Defines the id as the session that a host user has logged in
    id = session["hostusers_id"]

    # Queries the table parties and selects all the information from part where the host id is equal to host
    party_info = db.execute("SELECT * FROM party WHERE host_id=?", id)

    # Render the template hosthome.html and pass into the html page the party info from the table
    return render_template("hosthome.html", party_info=party_info)


# Party planner page: where hosts can create new parties
@app.route("/partyplanner", methods=["GET", "POST"])
@hostlogin_required
def partyplanner():
    # Define session id
    host_id = session["hostusers_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Set the variables
        party_name = request.form.get("party_name")
        start_date = request.form.get("start_date")
        start_time = request.form.get("start_time")
        end_date = request.form.get("end_date")
        end_time = request.form.get("end_time")
        venue = request.form.get("venue")
        listed = request.form.get("listed")
        other_details = request.form.get("other_details")

        # Check for invalid inputs; make sure user enters information for every input
        if not party_name:
            return apology("Please enter a Party Name")
        if not start_date:
            return apology("Please enter Start Date")
        if not start_time:
            return apology("Please enter Start Time")
        if not end_date:
            return apology("Please enter End Date")
        if not venue:
            return apology("Please enter the venue")
        if not listed:
            return apology("Please indicate whether the party is listed or unlisted")


        # Insert the data into the database (party.db)
        db.execute("INSERT INTO party (host_id, party_name, start_date, start_time, end_date, end_time, venue, listed, other_details) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    host_id, party_name, start_date, start_time, end_date, end_time, venue, listed, other_details)

        # Send user to invite page
        if listed == "Listed":
            return redirect("/invite")
        else:
            return redirect("/hosthome")

    # If access page via GET
    else:
        return render_template("partyplanner.html")


# Invite page: where hosts can invite other users to their "listed" parties
@app.route("/invite", methods=["GET", "POST"])
@hostlogin_required
def invite():
    # Define variable of session id
    host_id = session["hostusers_id"]

    # If the route is reached via POST
    if request.method == "POST":
        # Check that user inputted a username for the invitee
        if not request.form.get("inivitee_username"):
            return apology("Enter username(s)")

        # Initialized counters to check whether the input usernames exist/have already been invited
        check_int = 0
        check_exist = 0
        # Get user input
        party_name = request.form.get("party_name")
        # Check whether a party was selected
        if party_name == None:
            return apology("Select party")
        invitee_usernames = request.form.get("inivitee_username")
        # Takes out all of the spaces from the list
        invitee_usernames=invitee_usernames.replace(', ', ',').replace(' ,',',')
        party_id_listed = db.execute("SELECT id FROM party WHERE party_name=?", party_name)
        party_id = (party_id_listed[0]).get('id')
        # Change user input separated by commas into a list
        invitee_username_list = invitee_usernames.split(",")
        number = len(invitee_username_list)
        # Iterates over the list of usernames that have been input
        for i in range (number):
            username = invitee_username_list[i]
            username_check = db.execute("SELECT username FROM partyerusers WHERE username=?", username)
            for j in username_check:
                # Checks whether the entered user_ids exist
                if username == j["username"]:
                    check_exist = check_exist + 1
                    used = "unused"
                    invitee_id_listed = db.execute("SELECT id FROM partyerusers WHERE username=?", username)
                    invitee_id = (invitee_id_listed[0]).get('id')
                    # Checks whether the user has been invited already and only allows to invite those who have not been
                    checker = db.execute("SELECT * FROM invitation WHERE party_id=? AND partyer_id=?", party_id, invitee_id)
                    if not checker:
                        db.execute("INSERT INTO invitation (partyer_id, party_id, used) VALUES(?, ?, ?)",
                                    invitee_id, party_id, used)
                        check_int = check_int + 1
        if  check_exist != number:
            return apology("Some of the usernames you input did not exist. Users that exist have been invited. Return to Host Home to continue.")
        if check_int != number:
            return apology("Some people had already been invited. Return to Host Home to continue.")

        # Once done, redirect them to host home
        return redirect("/hosthome")

    # Initialize the page
    else:
        # Define session id
        host_id = session["hostusers_id"]

        # Define variable as listed to be as "listed"
        listed = "Listed"

        # Query table party in database where host_id matches and the party is listed
        party_list = db.execute("SELECT party_name FROM party WHERE host_id=? AND listed=?", host_id, listed)

        # Create an empty list named party
        party = []

        # For every party that is in the party table, append the party list
        for party_name in party_list:
            party.append(party_name['party_name'])

        # Define variable length as the length of the list called party
        length = len(party)

        # Render template invite.html and pass on the variables party_list and length
        return render_template("invite.html", party_list=party, length=length)


# Home page for partyers
@app.route("/partyerhome", methods=["GET", "POST"])
@partyerlogin_required
def partyerhome():
    # If route reached via POST
    if request.method == "POST":
        # Create variable for party selected by the user
        selected_party = request.form.get("selected_party")

        # Check that the user actually selected a party
        if not selected_party:
            return apology("Please select party to enter")

        # Create variable used defined as "used"
        used = "used"

        # Define variable for session
        id = session["partyerusers_id"]

        # Query the table party for the id where the party name
        party_id_listed = db.execute("SELECT id FROM party WHERE party_name=?", selected_party)

        # Create variable that defines the party id
        party_id = (party_id_listed[0]).get('id')

        # Update the table invitation so that used is now set to used for this partyer and party id
        db.execute("UPDATE invitation SET used=? WHERE partyer_id=? AND party_id=?", used, id, party_id)

        # Redirect the user to the partyer home page
        return redirect("/partyerhome")

    else:
        # Access the database for the info of the parties partyer is invited to
        id = session["partyerusers_id"]
        used = "unused"
        listed_parties = db.execute("SELECT * FROM party JOIN invitation ON party.id=invitation.party_id WHERE invitation.partyer_id=? AND invitation.used=?", id, used)

        # Access the database for the info of any open parties
        unlisted = "Unlisted"
        unlisted_parties = db.execute("SELECT * FROM party WHERE listed=?", unlisted)

        # Query database to get the party names for that users id and used invitation
        listed_party_list = db.execute("SELECT party_name FROM party JOIN invitation ON party.id=invitation.party_id WHERE invitation.partyer_id=? AND invitation.used=?", id, used)

        # Create an empty list called party and append the list for every party that has been queried
        party = []
        for party_name in listed_party_list:
            party.append(party_name['party_name'])
        length = len(party)

        # Return the template for partyer home, passing the variables for listed_parties, unlisted_parties, party_list, and length
        return render_template("partyerhome.html", listed_parties=listed_parties, unlisted_parties=unlisted_parties, party_list=party, length=length)


# Allows hosts to delete a party they have created
@app.route("/delete", methods=["GET", "POST"])
@hostlogin_required
def delete():
    # Defines session id
    host_id = session["hostusers_id"]

    # If route reached via POST
    if request.method == "POST":

        # Checks whether party is selected
        if request.form.get("party_name") == None:
            return apology("Select a party to delete")

        # Get user input, define them as variables
        party_name = request.form.get("party_name")
        party_id_listed = db.execute("SELECT id FROM party WHERE party_name=?", party_name)
        party_id = (party_id_listed[0]).get('id')

        # Query database for all information from the table invitation for that party id
        listed = db.execute("SELECT * FROM invitation WHERE party_id=?", party_id)

        # If the party selected is listed, delete that party from the table invitation
        if listed:
            db.execute("DELETE FROM invitation WHERE party_id=?", party_id)

        # Delete selected party from the table party
        db.execute("DELETE FROM party WHERE id=?", party_id)

        # Once done, redirect them to host home
        return redirect("/hosthome")

    # Initialize the page
    else:
        # Define variable for session
        host_id = session["hostusers_id"]

        # Query database for party names in party with that host id
        party_list = db.execute("SELECT party_name FROM party WHERE host_id=?", host_id)

        # Create an empty list called party, and append that list for every party name in the party list
        party = []
        for party_name in party_list:
            party.append(party_name['party_name'])
        length = len(party)

        # Return the template delete.html and pass on the variables party list and length
        return render_template("delete.html", party_list=party, length=length)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name)
# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
