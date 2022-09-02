from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

admin = Admin(app, name='NCP', template_mode='bootstrap3')

from app import db, routes, models
from app.models import User, Student, University, Grants
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Grants, db.session))
admin.add_view(ModelView(University, db.session))
#admin.add_view(ModelView(Grants, db.session))
# Add administrative views here

#app.run()