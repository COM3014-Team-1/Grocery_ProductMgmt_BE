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
        if not inspector.has_table("orders") or not inspector.has_table("order_product"):
            db.create_all()
            current_app.logger.info("Database tables created.")