from app import db, login
from flask_admin.menu import MenuLink
from flask import url_for, request, redirect
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user, login_required


class Users(UserMixin, db.Model):
    __tablename__ = 'USER' 
    User_Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(20), index=True, unique=True, nullable=False)
    Password_Hash = db.Column(db.String(180))

    def set_password(self, password):
        self.Password_Hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.Password_Hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.Username)

@login.user_loader
def load_user(Id):
    return Users.query.get(int(Id))

class SecureModelView(ModelView):
    """Custom view for all models. Login secured."""
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))
        
class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated  


class StudentsModelView(ModelView):
    """Custom view for Students. Login secured."""
    #searchable list. can add more
    column_searchable_list = ('Student_Number','First_Name','Last_Name', 'State')
    column_filters = ('Student_Id', 'Title', 'First_Name', 
    'Preferred_Name', 'Last_Name', 'Address_Line_One', 'Address_Line_Two', 'City', 'Postcode', 'State', 'Country', 'Date_Of_Birth', 'Phone_Number', 
    'Student_Email', 'Gender', 'BSB', 'Account_Number', 'Field_Of_Study', 'Country_Of_Birth','Indigenous_Australian', 'Disability', 'Aus_Citizen', 'Notes')
    
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class ProgramsModelView(ModelView):
    """Custom view for Programs. Login secured."""
    #searchable list. can add more
    column_searchable_list = ('Program_Id', 'Program_Name', 'Program_Acronym','Class_Code','Project_Code', 'ISEO_Code', 'Program_Type')
    column_filters = ('Program_Id', 'Program_Name', 'Program_Acronym', 'Year', 'Class_Code', 'Project_Code', 'ISEO_Code', 'UWA_Mobility_Grant_Project_Grant_Number',
    'UWA_Admin_Funding_Project_Grant_Number', 'Program_Type', 'Project_Status', 'Funding_Acquittal_Date', 'Project_Completion_Submission_Date',
    'Project_Completion_Report_Link', 'Refund_Utilisation_Commonwealth_Date', 'Commonwealth_Refund_Invoice_Link', 'Statutory_Decleration_Date',
    'Statutory_Decleration_Link', 'Original_Project_Schedule', 'Deed_Of_Variation_One', 'Deed_Of_Variation_Two', 'Deed_Of_Variation_Three',
    'Mobility_Grant_Funding_Received', 'Mobility_Grant_Dollar_Size', 'Mobility_Grant_Funding_Utilised', 'Mobility_Grant_Funding_Remaining',
    'Mobility_Grants_Received', 'Mobility_Grants_Utilised', 'Mobility_Grants_Remaining',
    'Internship_Grant_Funding_Received', 'Internship_Grant_Dollar_Size', 'Internship_Grant_Funding_Utilised', 'Internship_Grant_Funding_Remaining',
    'Internship_Grants_Received', 'Internship_Grants_Utilised', 'Internship_Grants_Remaining',
    'Language_Grant_Funding_Received', 'Language_Grant_Dollar_Size', 'Language_Grant_Funding_Utilised', 'Language_Grant_Funding_Remaining',
    'Language_Grants_Received', 'Language_Grants_Utilised', 'Language_Grants_Remaining',
    'Administration_Grant_Funding_Received', 'Administration_Grant_Dollar_Size', 'Administration_Grant_Funding_Utilised', 'Administration_Grant_Funding_Remaining',
    'Administration_Grants_Received', 'Administration_Grants_Utilised', 'Administration_Grants_Remaining',
    'Total_Grant_Funding_Received', 'Total_Grant_Dollar_Size', 'Total_Grant_Funding_Utilised', 'Total_Grant_Funding_Remaining',
    'Total_Grants_Received', 'Total_Grants_Utilised', 'Total_Grants_Remaining',
    'Notes')

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class PaymentsModelView(ModelView):
    """Custom view for Payments. Login secured."""
    #searchable list. can add more
    column_searchable_list = ("Payment_Id", "Student_Id", "Program_Id", "Payment_Amount")
    column_filters = ("Payment_Id", "Student_Id", "Program_Id", "UWA_Business_Unit", "Payment_Date", "Payment_Amount",
    "UWA_Account_Number", "Funding_Round", "Description")
   
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class UniversitiesModelView(ModelView):
    """Custom view for University. Login secured."""
    #searchable list. can add more
    column_searchable_list = ("University_Name", "University_Id", "ABN")
    column_filters = ("University_Id", "University_Name", "ABN", "Member_Status_2014", "Member_Status_2015", "Member_Status_2016", "Member_Status_2017",
    "Member_Status_2018", "Member_Status_2019", "Member_Status_2020", "Member_Status_2021", "Member_Status_2022")
   
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class CampusesModelView(ModelView):
    """Custom view for Campuses. Login secured."""
    #searchable list. can add more
    column_searchable_list = ('Campus_Id', 'Campus_Name', 'Campus_State')
    column_filters = ('Campus_Id', 'University_Id', 'Campus_Name', 'Campus_State')
    
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class GrantsModelView(ModelView):
    """Custom view for Grants. Login secured."""
    #searchable list. can add more
    column_searchable_list = ('Grant_Id', 'Program_Id', 'Student_Id', 'Payment_Id', 'University_Id', 'Campus_Id')
    column_filters = ('Grant_Id', 'Program_Id', 'Student_Id', 'Payment_Id', 'University_Id', 'Campus_Id', 'Awarded', 'Forms_Received')
    
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
    __tablename__ = 'STUDENTS' 
    Student_Id = db.Column(db.String(50), primary_key = True) 
    University_Id =  db.Column(db.String(50), db.ForeignKey('UNIVERSITIES.University_Id'))
    Campus_Id =  db.Column(db.String(50), db.ForeignKey('CAMPUSES.Campus_Id'))
    Student_Number = db.Column(db.Integer)
    Title = db.Column(db.String(50))
    First_Name = db.Column(db.String(50))
    Preferred_Name = db.Column(db.String(50))
    Last_Name = db.Column(db.String(50))
    Address_Line_One = db.Column(db.String(50))
    Address_Line_Two = db.Column(db.String(50))
    City = db.Column(db.String(50))
    Postcode = db.Column(db.Integer)
    State = db.Column(db.String(50))
    Country = db.Column(db.String(50))
    Date_Of_Birth = db.Column(db.Date)
    Phone_Number = db.Column(db.String(50))
    Student_Email = db.Column(db.String(100))
    Gender = db.Column(db.String(50))
    BSB = db.Column(db.String(50))
    Account_Number = db.Column(db.Integer)
    Field_Of_Study = db.Column(db.String(50))
    Country_Of_Birth =  db.Column(db.String(50))
    Indigenous_Australian = db.Column(db.Boolean) 
    Disability = db.Column(db.Boolean) 
    Aus_Citizen = db.Column(db.Boolean)
    Notes = db.Column(db.String(100))

    def __repr__(self):
        return '<Student {}>'.format(self.Student_Id, self.First_Name, self.Last_Name)



class Programs(db.Model):  
    __tablename__ = 'PROGRAMS' 
    Program_Id = db.Column(db.String(50), primary_key = True)
    Program_Name = db.Column(db.String(100))
    Program_Acronym = db.Column(db.String(50))
    Year = db.Column(db.Integer)
    Class_Code = db.Column(db.String(50))
    Project_Code = db.Column(db.String(50))
    ISEO_Code = db.Column(db.String(50))
    UWA_Mobility_Grant_Project_Grant_Number = db.Column(db.String(50))
    UWA_Admin_Funding_Project_Grant_Number = db.Column(db.String(50))
    Program_Type = db.Column(db.String(50))
    Project_Status = db.Column(db.String(50))

    Funding_Acquittal_Date = db.Column(db.Date)
    Project_Completion_Submission_Date = db.Column(db.Date)
    Project_Completion_Report_Link = db.Column(db.String)
    Refund_Utilisation_Commonwealth_Date = db.Column(db.Date)
    Commonwealth_Refund_Invoice_Link = db.Column(db.String)
    Statutory_Decleration_Date = db.Column(db.Date)
    Statutory_Decleration_Link = db.Column(db.String)
    Original_Project_Schedule = db.Column(db.String)
    Deed_Of_Variation_One = db.Column(db.String)
    Deed_Of_Variation_Two = db.Column(db.String)
    Deed_Of_Variation_Three = db.Column(db.String)

    Mobility_Grant_Funding_Received = db.Column(db.Integer)
    Mobility_Grant_Dollar_Size = db.Column(db.Integer)
    Mobility_Grant_Funding_Utilised = db.Column(db.Integer)
    Mobility_Grant_Funding_Remaining = db.Column(db.Integer)
    Mobility_Grants_Received = db.Column(db.Integer)
    Mobility_Grants_Utilised = db.Column(db.Integer)
    Mobility_Grants_Remaining = db.Column(db.Integer)

    Internship_Grant_Funding_Received = db.Column(db.Integer)
    Internship_Grant_Dollar_Size = db.Column(db.Integer)
    Internship_Grant_Funding_Utilised = db.Column(db.Integer)
    Internship_Grant_Funding_Remaining = db.Column(db.Integer)
    Internship_Grants_Received = db.Column(db.Integer)
    Internship_Grants_Utilised = db.Column(db.Integer)
    Internship_Grants_Remaining = db.Column(db.Integer)
    
    Language_Grant_Funding_Received = db.Column(db.Integer)
    Language_Grant_Dollar_Size = db.Column(db.Integer)
    Language_Grant_Funding_Utilised = db.Column(db.Integer)
    Language_Grant_Funding_Remaining = db.Column(db.Integer)
    Language_Grants_Received = db.Column(db.Integer)
    Language_Grants_Utilised = db.Column(db.Integer)
    Language_Grants_Remaining = db.Column(db.Integer)

    Administration_Grant_Funding_Received = db.Column(db.Integer)
    Administration_Grant_Dollar_Size = db.Column(db.Integer)
    Administration_Grant_Funding_Utilised = db.Column(db.Integer)
    Administration_Grant_Funding_Remaining = db.Column(db.Integer)
    Administration_Grants_Received = db.Column(db.Integer)
    Administration_Grants_Utilised = db.Column(db.Integer)
    Administration_Grants_Remaining = db.Column(db.Integer)

    Total_Grant_Funding_Received = db.Column(db.Integer)
    Total_Grant_Dollar_Size = db.Column(db.Integer)
    Total_Grant_Funding_Utilised = db.Column(db.Integer)
    Total_Grant_Funding_Remaining = db.Column(db.Integer)
    Total_Grants_Received = db.Column(db.Integer)
    Total_Grants_Utilised = db.Column(db.Integer)
    Total_Grants_Remaining = db.Column(db.Integer)

    Notes = db.Column(db.String)

    def __repr__(self):
        return '<Program {}>'.format(self.Program_Id, self.Program_Name, self.Class_Code)



class Payments(db.Model):  
    __tablename__ = 'PAYMENTS' 
    Payment_Id = db.Column(db.String(50), primary_key = True) 
    Student_Id = db.Column(db.String(50), db.ForeignKey('STUDENTS.Student_Id'))
    Program_Id = db.Column(db.String(50), db.ForeignKey('PROGRAMS.Program_Id'))
    UWA_Business_Unit = db.Column(db.Integer)
    Payment_Date = db.Column(db.Date)
    Payment_Amount = db.Column(db.Integer)
    UWA_Account_Number = db.Column(db.Integer)
    Funding_Round = db.Column(db.String(50))
    Description = db.Column(db.String)

    def __repr__(self):
        return '<Payments: {}>'.format(self.Payment_Id, self.Student_Id, self.Payment_Amount)



class Universities(db.Model):  
    __tablename__ = 'UNIVERSITIES' 
    University_Id = db.Column(db.String(50), primary_key = True) 
    University_Name = db.Column(db.String(100))
    ABN = db.Column(db.Integer)
    Member_Status_2014 = db.Column(db.Boolean)
    Member_Status_2015 = db.Column(db.Boolean)
    Member_Status_2016 = db.Column(db.Boolean)
    Member_Status_2017 = db.Column(db.Boolean)
    Member_Status_2018 = db.Column(db.Boolean)
    Member_Status_2019 = db.Column(db.Boolean)
    Member_Status_2020 = db.Column(db.Boolean)
    Member_Status_2021 = db.Column(db.Boolean)
    Member_Status_2022 = db.Column(db.Boolean)

    def __repr__(self):
        return '<University: {}>'.format(self.University_Id, self.University_Name)



class Campuses(db.Model):  
    __tablename__ = 'CAMPUSES' 
    Campus_Id = db.Column(db.String(50), primary_key = True) 
    University_Id = db.Column(db.String(50), db.ForeignKey('UNIVERSITIES.University_Id'))
    Campus_Name = db.Column(db.String(50))
    Campus_State = db.Column(db.String(50))

    def __repr__(self):
        return '<Campus: {}>'.format(self.Campus_Name)



class Grants(db.Model):  
    __tablename__ = 'GRANTS' 
    Grant_Id = db.Column(db.String(50), primary_key = True) 
    Program_Id = db.Column(db.String(50), db.ForeignKey("PROGRAMS.Program_Id"))
    Student_Id = db.Column(db.String(50), db.ForeignKey("STUDENTS.Student_Id"))
    Payment_Id = db.Column(db.String(50), db.ForeignKey("PAYMENTS.Payment_Id"))
    University_Id = db.Column(db.String(50), db.ForeignKey("UNIVERSITIES.University_Id"))
    Campus_Id = db.Column(db.String(50), db.ForeignKey("CAMPUSES.Campus_Id"))
    Awarded = db.Column(db.Boolean)
    Forms_Received = db.Column(db.Boolean)

    def __repr__(self):
        return '<Grant {}>'.format(self.Grant_Id, self.Program_Id, self.Student_Id)
        

