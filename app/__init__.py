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

migrate = Migrate(app, db,render_as_batch=True)

login = LoginManager(app)
login.login_view = 'login'


from app import db, routes, models
from app.models import Users, Students, Programs, Payments, Universities, Campuses, Grants, Eligibility, MyAdminIndexView, StudentsModelView, ProgramsModelView, PaymentsModelView, UniversitiesModelView, CampusesModelView, GrantsModelView, LogoutMenuLink, EligibilityModelView, InfoView
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
#add admin views for tables/models
admin = Admin(app, name='NCP', template_mode='bootstrap3', index_view=MyAdminIndexView()) # figure out how to remove home endpoint 
admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))
#admin.add_view(SecureModelView(Users, db.session))ss
admin.add_view(InfoView(name='Information', endpoint='info'))
admin.add_view(StudentsModelView(Students, db.session))
admin.add_view(ProgramsModelView(Programs, db.session))
admin.add_view(PaymentsModelView(Payments, db.session))
admin.add_view(UniversitiesModelView(Universities, db.session))
admin.add_view(CampusesModelView(Campuses, db.session))
admin.add_view(GrantsModelView(Grants, db.session))
#admin.add_view(EligibilityModelView(Eligibility, db.session))




#app.run()