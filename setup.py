"""
NOTE: SETUP BASED OFF OF setup.py IN COMMUNITY BANK FLASK APP
ALL CREDIT TO ORIGINAL AUTHORS
"""

import os

from userdb import Db

#single db
DIRS = ['instance/var/db']

if __name__ == '__main__':

    print("Creating directories...")
    for d in DIRS:
        try:
            os.makedirs(d)
        except FileExistsError:
            pass

    print("Initializing database...")
    Db.setup()

    print("Done!")
