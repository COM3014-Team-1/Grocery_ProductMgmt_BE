from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from flask import current_app

db = SQLAlchemy()

def init_db(app):
    """Initializes the database and creates tables if they don't exist."""
    db.init_app(app)
    with app.app_context():
        engine = db.engine
        inspector = inspect(engine)
        
        required_tables = {"products", "categories"}
        existing_tables = set(inspector.get_table_names())
        
        if not required_tables.issubset(existing_tables):
            db.create_all()
            current_app.logger.info("Product & Category tables created.")
        else:
            current_app.logger.info("Database tables already exist.")
