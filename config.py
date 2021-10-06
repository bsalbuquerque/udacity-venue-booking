# ----------------------------------------------------------------------------#
# Config.
# ----------------------------------------------------------------------------#

import os
SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Disable track modifications, echo and CSRF
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
WTF_CSRF_ENABLED = False

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/fyyur'
