from flask import Flask
from apps.utils.db import db, init_db
from config import appsettings, Config
from flask_migrate import Migrate
from apps.controllers.productController import product_bp
from apps.controllers.categoryController import category_bp
from apps.config.loggerConfig import configure_logger
from apps.config.swaggerConfig import setup_swagger
from flask_jwt_extended import JWTManager
from apps.utils.seeder import seed_database

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)
    migrate = Migrate(app, db)

    configure_logger(app)
    setup_swagger(app)
    JWTManager(app)

    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)

    with app.app_context():
        seed_database()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port='5000', debug=True)