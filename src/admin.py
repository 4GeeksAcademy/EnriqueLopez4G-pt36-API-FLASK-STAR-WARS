import os
from flask_admin import Admin
from models import db, User,Character,Planet,Favorite
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))  # Vista para el modelo User
    admin.add_view(ModelView(Character, db.session))  # Vista para el modelo Character
    admin.add_view(ModelView(Planet, db.session))  # Vista para el modelo Planet
    admin.add_view(ModelView(Favorite, db.session))  # Vista para el modelo Favorite

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))