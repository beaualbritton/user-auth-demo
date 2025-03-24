
"""
BEAU ALBRITTON
CYBERSECURITY PRINCIPLES
FINAL LAB FLASK APP
"""
#importing dependencies
#flask first
from flask import Flask, render_template, request, url_for, redirect
#hashing functions from module 8
from password_crack import hash_pw, authenticate
#utility scripts i created 
import generate_password as generate 
from sanitize import sanitize

#see usedb for changes
from userdb import Db

app = Flask(__name__,static_folder='static')

#globals for login 
LOGIN_ATTEMPTS = 0
LOCKED_OUT = False

"""
USER HOME PAGE
"""
@app.route("/", methods=['GET', 'POST'])
def home():
    """Company Home page."""
    return render_template('home.html',
                           title="Home Page",
                           heading="Company Home Page")


"""
LOGIN PAGE
"""
@app.route("/login", methods=['GET', 'POST'])
def login():

    #using global keyword to track attemots, otherwise scope errors are thrown in following try/catch
    global LOGIN_ATTEMPTS, LOCKED_OUT;

    #checking form posted to server
    if request.method == 'POST':
        #sanitizing (see sanitize.py)
        username = sanitize(request.form.get('username'))
        password = sanitize(request.form.get('password'))
        
        #using userdb for connection
        conn = Db.get_connection()
        c = conn.cursor()

        try:
            # Simple SELECT query to find user, syntax roughly modeled from catamount community bank, bank.py
            c = Db.execute_query(conn,query = f'SELECT * FROM users WHERE username = "{username}"')
            user = c.fetchone()

            # Successful login
            if user and authenticate(user[2], password):
                
                return render_template('dashboard.html',title="Login Secure!",username=username,role=user[3])
            
            #Now locked out
            elif (LOGIN_ATTEMPTS >=3):
                LOCKED_OUT = True
            #Otherwise increase attempts and display alert to user
            else:
                LOGIN_ATTEMPTS+=1
                return render_template('login.html',
                                   title="Secure Login",
                                   heading="Secure Login",
                                   error=f"Invalid username or password",
                                   alert=f"{4-LOGIN_ATTEMPTS} Attempts remaining before lock out.")
        
        #Handling any exception as an error and rendering it for the user to see.
        except Exception as error:
            return render_template('login.html',
                                   title="Secure Login",
                                   heading="Secure Login",
                                   error=f"Login error: {str(error)}")
        
    #Rendering login each time and checking if locked out as well
    return render_template('login.html',
                           title="Secure Login",
                           heading="Secure Login",
                           locked=LOCKED_OUT)
"""
REGISTER PAGE
"""
@app.route("/register", methods=['GET', 'POST'])
def register():
    #Checking for posted form 
    if request.method == 'POST':
        username = sanitize(request.form.get('username'))
        password = sanitize(request.form.get('password'))

        # Checking if generate password button was clicked
        if 'generate_password' in request.form:
            #Generate a password with complexity requirements, see generate_password.py
            generated_password = generate.generate_strong_password()
            #Then rendering it to the user
            return render_template('register.html',
                                   title="Register",
                                   heading="Register New Account",
                                   generated_password=generated_password,
                                   password=generated_password)

        #Otherwise, username and password were submitted
        if username and password:
            # Basic password complexity check, see generate_password.py
            if not (generate.check_password_strength(password)):
                return render_template('register.html',
                                       title="Register",
                                       heading="Register New Account",
                                       error="Password does not meet complexity requirements")

            # Hash password with code from module 8 
            password_hash = hash_pw(password)

            # Connect to database with Db methods
            conn = Db.get_connection()
            c = conn.cursor()

            try:
                # Simple INSERT query for users table
                c = Db.execute_query(conn,query = f'INSERT INTO users (username, pwhash, role) VALUES ("{username}", "{password_hash}", "guest")')
                conn.commit()
                #After adding, redirects to homepage.
                return redirect(url_for('home'))

            #Checks for error (see userdb.py, technically SQLITE3.ERROR)
            except Db.ERROR:
                return render_template('register.html',
                                       title="Register",
                                       heading="Register New Account",
                                       error="Username already exists, or registration failed. Try again.")
    #Basic rendering for register
    return render_template('register.html',
                           title="Register",
                           heading="Register New Account")

if __name__ == '__main__':
    app.run(debug=True)