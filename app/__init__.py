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


from app import db, routes, models
from app.models import Users, Students, Universities, Campuses, Grants, SecureModelView, MyAdminIndexView, UniversityModelView
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
#add admin views for tables/models
admin = Admin(app, name='NCP', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(SecureModelView(Users, db.session))
admin.add_view(SecureModelView(Students, db.session))
admin.add_view(SecureModelView(Grants, db.session))
admin.add_view(UniversityModelView(Universities, db.session))
admin.add_view(SecureModelView(Campuses, db.session))



#app.run()