import os
from flask import Flask, render_template_string
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join('html', filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

class ConfigClass(object):
    # Flask settings
    SECRET_KEY =              os.getenv('SECRET_KEY',       'sdfhq34ty0q98ruihql34t9q04')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',     'sqlite:///hatchr.sqlite')
    CSRF_ENABLED = True

    # Flask-Mail settings
    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'hatchrapp@gmail.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'kathyesha')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"HatchrAdmin" <hatchrapp@gmail.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.gmail.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))

    # Flask-User settings
    USER_APP_NAME        = "Hatchr"                # Used by email templates

    # SQL-Alchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = True


def create_app():
    """ Flask application factory """
    
    # Setup Flask app and app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Initialize Flask extensions
    db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy
    mail = Mail(app)                                # Initialize Flask-Mail

    # Define the User data model. Make sure to add flask.ext.user UserMixin !!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)

        # User authentication information
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, server_default='')
        reset_password_token = db.Column(db.String(100), nullable=False, server_default='')

        # User email information
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())

        # User information
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
        first_name = db.Column(db.String(100), nullable=False, server_default='')
        last_name = db.Column(db.String(100), nullable=False, server_default='')

    # Create all database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
    user_manager = UserManager(db_adapter, app)     # Initialize Flask-User

    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        return get_file('index.html')

    # The Members page is only accessible to authenticated users
    @app.route('/user/<username>')
    @login_required                                 # Use of @login_required decorator
    def members_page(username):
        return get_file('login.html')

    return app

# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)