import email
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

from .enums import Roles_enum

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .auth import auth
    from .report import report
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(report, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        from .models import User, Role, Group, Tag

        admin = Role(id=Roles_enum.ADMIN.value, role=Roles_enum.ADMIN.name)
        user = Role(id=Roles_enum.USER.value, role=Roles_enum.USER.name)
        admin_user = User(email= "Ghanim@gmail.com", password=generate_password_hash("admin1234", method='sha256'), role_id=admin.id)
        with app.app_context():
            db.session.add(admin)
            db.session.add(user)
            db.session.add(admin_user)
            db.session.commit()

        groups = ["Saudi Arabia", "US", "General"]
        with app.app_context():
            for g in groups:
                group = Group(name=g)
                db.session.add(group)
            db.session.commit()     

        tags = ["Technology", "Sports", "Medical"]
        with app.app_context():
            for t in tags:
                tag = Tag(name=t)
                db.session.add(tag)
            db.session.commit()   

        print('Created Database!')