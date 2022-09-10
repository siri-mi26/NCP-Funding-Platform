from app import db, login
from flask_admin.menu import MenuLink
from flask import url_for, request, redirect
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user, login_required


class Users(UserMixin, db.Model):
    __tablename__ = 'user' 
    """temp create login user table with sqlite.
    can be removed when boys are done with db
    unless we decide to keep"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(180))
    #email should probs/could be included & auth level. But not must have

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))

class SecureModelView(ModelView):
    """Custom view for all models. Login secured."""
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))
        
class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated  

class UniversityModelView(ModelView):
    """Custom view for University. Login secured."""
    #searchable list. can add more
    column_searchable_list = ('University_Name', 'id', "ABN")
    column_filters = ('University_Name', 'id', "ABN", "Member_Status_2014", "Member_Status_2015", "Member_Status_2016", "Member_Status_2017",
    "Member_Status_2018", "Member_Status_2019", "Member_Status_2020", "Member_Status_2021", "Member_Status_2022")
   
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class StudentModelView(ModelView):
    """Custom view for Student. Login secured."""
    #searchable list. can add more
    column_searchable_list = ('student_Number', 'University.University_Name', 'Campus.Campus_Name','First_Name','Last_Name', 'Prefered_Name', 'Age','Adress_Line_One', 'Adress_Line_Two', 'City', 'State', 'Nationality', 'Notes')
    column_filters = ('id', 'student_Number','University.University_Name','Campus.Campus_Name','University_ID', 'Campus_ID', 'First_Name', 'Last_Name', 'Prefered_Name', 'Title', 'Age', 'Adress_Line_One', 'Adress_Line_Two',
    'City','State', 'Nationality', 'Phone_Number', 'BSB', 'Account_Number', 'Country_Of_Birth','Indigenous_or_Torres_Strait_Australian','Disability')
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class CampusModelView(ModelView):
    """Custom view for Student. Login secured."""
    #searchable list. can add more
    column_searchable_list = ('Campus_Name', 'Campus_State','University.University_Name')
    column_filters = ('id', 'Campus_Name', 'Campus_State','University.University_Name')
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))
class MyAdminIndexView(AdminIndexView):
    """Custom view for index. Login secured."""
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))
    @expose('/')
    def index(self):
        if not current_user.is_authenticated and current_user.is_admin:
            return redirect(url_for('auth.login'))
        return super(MyAdminIndexView, self).index()


class Students(db.Model):  
    __tablename__ = 'student' 
    id = db.Column(db.Integer, primary_key = True) 
    student_Number = db.Column(db.Integer)
    University_ID =  db.Column(db.Integer, db.ForeignKey('university.id'))
    Campus_ID =  db.Column(db.Integer, db.ForeignKey('campus.id'))
    University = db.relationship("Universities")
    Campus= db.relationship("Campuses")
    First_Name = db.Column(db.String(50))
    Last_Name = db.Column(db.String(50))
    Prefered_Name = db.Column(db.String(50))
    Title = db.Column(db.String(50))
    Age = db.Column(db.Integer)
    Adress_Line_One = db.Column(db.String(50))
    Adress_Line_Two = db.Column(db.String(50))
    City = db.Column(db.String(50))
    State = db.Column(db.String(50))
    Nationality = db.Column(db.String(50))
    Phone_Number = db.Column(db.Integer)
    BSB = db.Column(db.Integer)
    Account_Number = db.Column(db.Integer)
    Country_Of_Birth =  db.Column(db.String(50))
    Indigenous_or_Torres_Strait_Australian = db.Column(db.Boolean) 
    Disability = db.Column(db.Boolean) 
    AUS_Citizen = db.Column(db.Boolean)
    Notes = db.Column(db.String(50))

    def __repr__(self):
        return '<Student {}>'.format(self.studentnumber)

class Universities(db.Model):  
    __tablename__ = 'university' 
    id = db.Column(db.Integer, primary_key = True) 
    University_Name = db.Column(db.String)
    ABN = db.Column(db.Integer)
    Member_Status_2014 = db.Column(db.Boolean)
    Member_Status_2015 = db.Column(db.Boolean)
    Member_Status_2016 = db.Column(db.Boolean)
    Member_Status_2017= db.Column(db.Boolean)
    Member_Status_2018 = db.Column(db.Boolean)
    Member_Status_2019 = db.Column(db.Boolean)
    Member_Status_2020 = db.Column(db.Boolean)
    Member_Status_2021 = db.Column(db.Boolean)
    Member_Status_2022 = db.Column(db.Boolean)

    def __repr__(self):
        return '<University: {}>'.format(self.University_Name)

class Campuses(db.Model):  
    __tablename__ = 'campus' 
    id = db.Column(db.Integer, primary_key = True) 
    University_ID = db.Column(db.Integer, db.ForeignKey("university.id"))
    University = db.relationship("Universities")
    Campus_Name = db.Column(db.String(50))
    Campus_State = db.Column(db.String(50))

    def __repr__(self):
        return '<Campus: {}>'.format(self.Campus_Name)

class Grants(db.Model):  
    __tablename__ = 'Grants' 
    id = db.Column(db.Integer, primary_key = True) 
    Name = db.Column(db.Integer)

    def __repr__(self):
        return '<Grant {}>'.format(self.Name)
        

