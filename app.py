from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_login import LoginManager
import os
from flask_migrate import Migrate
import logging

# Configure log file location and format
log_file = 'app.log'
log_format = '%(asctime)s [%(levelname)s] - %(message)s'
logging.basicConfig(filename=log_file, level=logging.INFO, format=log_format)

app = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
      app.logger.info("Currently no production config is setup.")
      raise Exception("Currently no production config is setup.")
    else:
      app.logger.debug("Staring Local Development.")
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    migrate = Migrate(app, db)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'
    login_manager.login_message = 'Please login first'

    from application.models import User 
    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(user_id)

    app.app_context().push()
    app.logger.info("App setup complete")
    return app

app = create_app()


from application.controllers import *

if __name__ == '__main__':
    app.run(debug = True)
