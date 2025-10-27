from flask import Flask
from firebase_admin import credentials, initialize_app

cred = credentials.Certificate("C:/SD/api/key.json")
default_app = initialize_app(cred)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'NinjrUHVCQGAHvEb2Ual59nVCtMD0zEouUw7i8rv'

    from .userAPI import userAPI
    app.register_blueprint(userAPI, url_prefix='/user')
    return app