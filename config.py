import os
import json

def load_config():
    env = os.getenv('FLASK_ENV', 'development').lower()  # Get the current environment
    config_file = f'config/appsettings.{env}.config'  # Load the respective config file
    
    with open(config_file) as file:
        config = json.load(file)
    return config

appsettings = load_config()

class Config:
    SQLALCHEMY_DATABASE_URI = appsettings['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = appsettings['DEBUG']

