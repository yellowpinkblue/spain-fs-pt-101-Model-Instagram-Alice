import os
from flask_admin import Admin
from models import db, Users, Profiles, Post, Comment, Follow
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(Users, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))

    #(1 de 4) Models Instagram - Profile
    admin.add_view(ModelView(Profiles, db.session))
    #(2 de 4) Models Instagram - Post
    admin.add_view(ModelView(Post, db.session))
    #(3 de 4) Models Instagram - Comment
    admin.add_view(ModelView(Comment, db.session))
    #(4 de 4) Models Instagram - Follow
    admin.add_view(ModelView(Follow, db.session))