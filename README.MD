# SECURE LOGIN DEMO
### Beau Albritton
#### NOTE: ALL CREDIT TO JIM EDDY FOR CODE/PROVIDED IN 
 https://gitlab.uvm.edu/James.Eddy/cs-2660-catamount-community-bank


To install a clean, fresh database, run setup.py, otherwise the database I have been working on will be used. Found in `instance/var/db/users.db`

After dependencies are installed, run main.py from the terminal and navigate to the browser on the IP address served to the user.
From there, you can login, which sends you to the dashboard (if successful) or locks you out after 3 failed attempts. You can also register with the /register webpage, which has it's own generate password functionality. All inputs are sanitized and validated.


For specific questions related to my code, I tried to document things obsessively, each file has at least some comment(s) explaining it's purpose. main.py contains all relevant flask code, where generate_password.py, password_crack.py, userdb.py, and sanitize.py are all helper/utility programs that are later called inside main.py. HTML templates can be found in `/templates` Again, database can be found in `instance/var/db/users.db`.


