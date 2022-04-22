-bouncer.db
We created 1 database with 4 tables in total, on https://www.phpliteadmin.org/. The tables were hostusers.db, partyerusers.db, party.db, and invitation.db. The columns in each table were as follows:
    -hostusers.db
        id (primary key, int not null)
        username (text, not null)
        hash (text, not null) -- this is the hashed password
        email (text, not null)
    -partyerusers.db
        id (primary key, int not null)
        username (text, not null)
        hash (text, not null) -- this is the hashed password
        email (text, not null)
    -party.db
        id (integer, primary key, not null)
        host_id (integer, not null)
        party_name (text, not null)
        start_date (datetime, not null)
        start_time (datetime, not null)
        end_date (datetime, not null)
        end_time (datetime, not null)
        venue (text, not null)
        listed (text, not null) -> only takes either “Listed” or “Unlisted” by implementing a dropdown option in partyplanner page
        other_details (text, not null)
    -invitation.db
        invite_code (we ended up not using this, but phpliteadmin was down so couldn't change it)
        partyer_id (integer, not null)
        party_id (integer, not null)
        used (text, not null) -> only takes either “used” or “unused” using the python code in app.py

-layout.html
We utilized flask in order to use python with html and css. We first created a layout.html page which gives the baseline layout for all the other html pages. Layout.html was taken from our layout.html from pset9 (finance) and altered to fit our needs for this assignment. We coded layout.html so that it shows certain icons depending on whether a user is logged in or not. We used jinja syntax in order to incorporate these if statements. If a host has logged in, then the icons for host home (which redirect the user to the host home page--/hosthome, hosthome.html) and log out (which clears the session and redirects the user to /, index.html. If a partyer is logged in, then, similarly, the icons for partyer home, which redirects the user to /partyerhome, partyerhome.html, and log out, which has the same functionality as log out for hosts. Lastly, for all other cases (when no user is logged in) there are four icons: host register (redirects to /hostregister, hostregister.hml), partyer register (redirects to /partyerregister, partyerregister.html), host login (redirects to /hostlogin, hostlogin.html) and partyer log in (redirects to /partyerlogin, partyerlogin.html)

-index.html and def index() in app.py
The index page was implemented so that it shows a welcome message to those who are not logged in yet or who have logged out.

-hostlogin.html, partyerlogin.html, and their corresponding python functions in app.py
The hostlogin and partyerlogin functions in app.py are adapted from the code used in pset9 (finance). It first clears the session, and, if the request method is POST, it checks if the user entered a username and password. If not, it returns an apology message. It then queries the corresponding table (queries the hostusers table if a host is logging in or partyerusers table if a partyer is logging in), selecting all the information from the row of the table with the username entered by the user. If the number of rows is not equal to 1 or if the hashed password in the table does not match the one inputted by the user (we used the check_password_hash function to compare the hashed password in the table with the password inputted by the table), then an apology is returned. Then, the user which has logged in is remembered using session, and this varies slightly depending on whether the user is a host or partyer, reading as session[“hostusers_id”] for hosts and session[“partyerusers_id”] for partyers. This is set equal to the id of the first row of the corresponding table in order to be able to refer to what session is being used at the moment. Lastly, the user is redirected to the host home page (/hosthome) if the login is for hosts and partyer home page (/partyerhome) if the login is for partyers. If the user reaches the route via GET, then the template for the login page is rendered (partyerlogin.html for partyers and hostlogin.html for hosts).

The html pages for logging in: hostlogin.html and partyerlogin.html are both adapted from the login.html page from pset9 and are identical to one another. Both hostlogin.html and partyerlogin.html have text boxes to input username and password, as well as a submit button to log in.

-hostregister.html, partyerregister.html, and their corresponding python functions in app.py
The hostregister and partyerregister functions in app.py are similar except for the table in which they insert the data inputted. These functions were also derived from our code in pset9. For users registering as hosts, the information they have inputted is inserted into the hostusers table in the bouncer database. For users registering as partyers, the information they have inputted is inserted into the partyerusers table in the bouncer database. Aside from this, the two functions are the same. They both check if the user has inputted a username, and that this username does not already exist within the database. It also checks if the user has inputted an email address and a password. Furthermore, there are several security checks put into place to make sure the password the user creates is strong enough; thus, this function checks if the password has a minimum length of 6 characters, has at least one number, one uppercase letter, one lowercase letter, and one symbol. Then, the user must confirm the password, and this function checks if the confirmation matches the original password entered. If the user does not meet any of these requirements, an apology message is returned. If the user does meet all of the requirements, the password entered by the user is hashed using the function generate_password_hash and the username inputted, the hashed password, and the email inputted are all inserted to the corresponding table and columns (values it represents). After they are registered, it ultimately redirects the user to their corresponding login page. If the user reaches the route via GET, then the template for register is rendered (partyerregister.html for partyers and hostregister.html for users).

The register html pages, partyerregister.html and hostregister.html are both the same and taken from our register.html code in pset9. This page creates a text box for username, email, password, and password confirmation, as well as a submit button to register the user.

-apology.html and its uses throughout app.py
We created an apology function in helpers.py, which was inspired by the apology helper function in pset9. This function takes in an argument, called message, and it renders the template apology.html with the variable message, which is set equal to the argument message. The corresponding apology.html page uses bootstrap to show a “danger” alert--a red box--with message being printed inside of it. This page also has a back button which allows the user to go back to the page he/she was in before getting the apology message. The purpose of apology is to tell the user when they have made a mistake and ensure that they are inputting everything they need to input.

-logout
The logout() function is designed to clear the current session and redirect the user to the index page

-hosthome.html and their corresponding python functions in app.py
The function for hosthome.html selects all the parties from party.db with a host_id that matches the hostuser id of the user currently logged in, and sends the values to the hosthome.html page. The html then shows the information as a table using jinja that iterates over the dictionary sent to the html page. Below the table, there are 3 buttons, “Invite” “Create a Party!” and “Delete a Party.” Each one is a form that redirects the user to “/invite” “/partyplanner” and “/delete,” respectively.

-invite.html and their corresponding python functions in app.py
The function for invite.html initializes the page by selecting all the party names from party.db where host_id is the id of the host user that is currently and listed is set to “Listed.” Then, we render the template, sending the list of party names to the page, and showing them as a drop down menu using jinja and iterating over the list. When the user selects the party they want to invite people to and enters the usernames of the people they want to invite, the function takes in the input (party_name, and list of usernames). Then, it creates a python list by separating the input list of username at their commas using .split. Then it iterates through the list to check whether the user exists, and if they do whether they have been invited to the party before. If they haven’t, it inserts the invitation for that partyeruser in invitation.db for that party_name. Lastly, the function either returns an apology saying the user input a username that doesn't exist, apology saying there were people that were already invited in their list, or redirects the host users to the hosthome page if there were no errors.

-partyplanner.html and their corresponding python functions in app.py
The function takes in all the values that the user inputs in the form on partyplanner.html and inserts them into the table party in bouncer.db to record a new party. The function redirects the user to “/invite” so that they can invite people to the party they just created, or “/apology” saying they havent input values for all of the columns (except “other details” which can be left blank) depending on the condition.

-delete.html and their corresponding python functions in app.py
The function initializes the page the same way the function for invite.html does. When the user clicks delete, it will take the name of the party as an input, and delete the party from the table party using db.execute, and also delete all the invitations corresponding to those parties from the table invitation. Lastly, it will return the user to “/hosthome” or “/apology” with an input of message saying that the user has not selected a party from the dropdown, depending on the condition.

-partyerhome.html and their corresponding python functions in app.py
The function for partyerhome takes all the listed parties that the user has been invited to, by selecting the party information of the parties that have invitations with the partyer_id that matches the current user’s and has not been used (using SELECT * FROM party JOIN invitation ON party.id=invitation.party_id WHERE invitation.partyer_id=? AND invitation.used=?", id, used). Then, it prints out that information as a table on the html page using jinja, and does  the same for all the unlisted parties, where the values selected is all the parties that have been created and set listed=”Unlisted”. The enter button on the bottom of the page essentially deactivates the invitation of the party the user is entering. We do this by updating the used column in the table invitation for the party the user selected to enter to “used”. By doing so, the invitation does not show up on the partyer’s home page anymore.
