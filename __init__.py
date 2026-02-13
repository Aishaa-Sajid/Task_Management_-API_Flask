from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
# This __init.py turns a folder into a Python package.
db=SQLAlchemy()
migrate=Migrate()

def create_app():   #initializes the Database (db) and Migrations (migrate), then hooks up the "Blueprints"
    app=Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)

    from app.routes.auth import auth_bp
    from app.routes.categories import category_bp
    from app.routes.tasks import task_bp

    app.register_blueprint(auth_bp,url_prefix="/api/auth")   #sub-modules for Tasks, Auth, and Categories
    app.register_blueprint(task_bp,url_prefix="/api/tasks")
    app.register_blueprint(category_bp,url_prefix="/api/categories")

    return app