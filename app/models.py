from app import db, login
from flask_admin.menu import MenuLink
from flask import url_for, request, redirect
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user, login_required
import pandas as pd
from datetime import datetime
import io
import requests
from sqlalchemy import VARCHAR, create_engine
from config import  Config    



class Users(UserMixin, db.Model):
    __tablename__ = 'USER' 
    id = db.Column(db.Integer, primary_key=True)
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

    can_export = True 
    #searchable list. can add more
    column_searchable_list = ('Student_Number','First_Name', 'Title','Last_Name', 'State', 'Country', 'Gender')

    column_list = ('Student_Id', 'University_Id','Campus_Id', 'Student_Number','Title', 'First_Name', 
    'Preferred_Name', 'Last_Name', 'Address_Line_One', 'Address_Line_Two', 'City', 'Postcode', 'State', 'Country', 'Date_Of_Birth', 'Phone_Number', 
    'Student_Email', 'Gender', 'BSB', 'Account_Number', 'Field_Of_Study', 'Country_Of_Birth','Indigenous_Australian', 'Disability', 'Aus_Citizen', 'Notes')
    
    form_columns = ('Student_Id','University_Id','Campus_Id', 'Student_Number', 'Title', 'First_Name',  
    'Preferred_Name', 'Last_Name', 'Address_Line_One', 'Address_Line_Two', 'City', 'Postcode', 'State', 'Country', 'Date_Of_Birth', 'Phone_Number', 
    'Student_Email', 'Gender', 'BSB', 'Account_Number', 'Field_Of_Study', 'Country_Of_Birth','Indigenous_Australian', 'Disability', 'Aus_Citizen', 'Notes')

    column_filters = ('Student_Id','University_Id','Campus_Id', 'Student_Number', 'Title', 'First_Name', 
    'Preferred_Name', 'Last_Name', 'Address_Line_One', 'Address_Line_Two', 'City', 'Postcode', 'State', 'Country', 'Date_Of_Birth', 'Phone_Number', 
    'Student_Email', 'Gender', 'BSB', 'Account_Number', 'Field_Of_Study', 'Country_Of_Birth','Indigenous_Australian', 'Disability', 'Aus_Citizen', 'Notes')
    
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class ProgramsModelView(ModelView):
    """Custom view for Programs. Login secured."""
    can_export = True 

    column_searchable_list = ('Program_Id', 'Program_Name', 'Program_Acronym', 'Program_Type')

    column_list = ('Program_Id', 'Program_Name', 'Program_Acronym', 'Year', 'Class_Code', 'Project_Code', 'ISEO_Code', 'UWA_Mobility_Grant_Project_Grant_Number',
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
    'Total_Grant_Funding_Received', 'Total_Grant_Funding_Utilised', 'Total_Grant_Funding_Remaining',
    'Total_Grants_Received', 'Total_Grants_Utilised', 'Total_Grants_Remaining',
    'Notes')

    form_columns = ('Program_Id', 'Program_Name', 'Program_Acronym', 'Year', 'Class_Code', 'Project_Code', 'ISEO_Code', 'UWA_Mobility_Grant_Project_Grant_Number',
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
    'Total_Grant_Funding_Received', 'Total_Grant_Funding_Utilised', 'Total_Grant_Funding_Remaining',
    'Total_Grants_Received', 'Total_Grants_Utilised', 'Total_Grants_Remaining',
    'Notes')

    
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
    'Total_Grant_Funding_Received', 'Total_Grant_Funding_Utilised', 'Total_Grant_Funding_Remaining',
    'Total_Grants_Received', 'Total_Grants_Utilised', 'Total_Grants_Remaining',
    'Notes')

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class PaymentsModelView(ModelView):
    """Custom view for Payments. Login secured."""
    #searchable list. can add more
    can_export = True 

    column_searchable_list = ()

    column_list = ("Payment_Id", "Student_Id", "Program_Id", "UWA_Business_Unit", "Payment_Date", "Payment_Amount",
    "UWA_Account_Number", "Funding_Round", "Description")

    form_columns = ("Payment_Id", "Student_Id", "Program_Id", "UWA_Business_Unit", "Payment_Date", "Payment_Amount",
    "UWA_Account_Number", "Funding_Round", "Description")
   
    column_searchable_list = ("Payment_Id", "Student_Id", "Program_Id", "Description")
    
    column_filters = ("Payment_Id", "Student_Id", "Program_Id", "UWA_Business_Unit", "Payment_Date", "Payment_Amount",
    "UWA_Account_Number", "Funding_Round", "Description")
   
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class UniversitiesModelView(ModelView):
    """Custom view for University. Login secured."""
    can_export = True 

    column_searchable_list = ("University_Id","University_Name")

    column_list =  ("University_Id", "University_Name", "ABN", "Member_Status_2014", "Member_Status_2015", "Member_Status_2016", "Member_Status_2017",
    "Member_Status_2018", "Member_Status_2019", "Member_Status_2020", "Member_Status_2021", "Member_Status_2022","Member_Status_2023", "Member_Status_2024",
    "Member_Status_2025", "Member_Status_2026", "Member_Status_2027", "Member_Status_2028", "Member_Status_2029", "Member_Status_2030")
    
    form_columns =  ("University_Id", "University_Name", "ABN", "Member_Status_2014", "Member_Status_2015", "Member_Status_2016", "Member_Status_2017",
    "Member_Status_2018", "Member_Status_2019", "Member_Status_2020", "Member_Status_2021", "Member_Status_2022","Member_Status_2023", "Member_Status_2024",
    "Member_Status_2025", "Member_Status_2026", "Member_Status_2027", "Member_Status_2028", "Member_Status_2029", "Member_Status_2030")
    
    column_filters = ("University_Id", "University_Name", "ABN", "Member_Status_2014", "Member_Status_2015", "Member_Status_2016", "Member_Status_2017",
    "Member_Status_2018", "Member_Status_2019", "Member_Status_2020", "Member_Status_2021", "Member_Status_2022","Member_Status_2023", "Member_Status_2024",
    "Member_Status_2025", "Member_Status_2026", "Member_Status_2027", "Member_Status_2028", "Member_Status_2029", "Member_Status_2030")
   
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class CampusesModelView(ModelView):
    """Custom view for Campuses. Login secured."""
    can_export = True 

    column_searchable_list = ('Campus_Id', 'University_Id', 'Campus_Name', 'Campus_State')

    column_list = ('Campus_Id', 'University_Id', 'Campus_Name', 'Campus_State')

    form_columns = ('Campus_Id', 'University_Id', 'Campus_Name', 'Campus_State')

    column_filters = ('Campus_Id', 'University_Id', 'Campus_Name', 'Campus_State')
    
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class GrantsModelView(ModelView):
    """Custom view for Grants. Login secured."""
    #searchable list. can add more
    can_export = True 

    column_searchable_list = ('Grant_Id', 'Program_Id', 'Student_Id', 'Payment_Id', 'University_Id', 'Campus_Id')
    
    column_list = ('Grant_Id', 'Program_Id', 'Student_Id', 'Payment_Id', 'University_Id', 'Campus_Id', 'Awarded', 'Forms_Received')
    
    form_columns = ('Grant_Id', 'Program_Id', 'Student_Id', 'Payment_Id', 'University_Id', 'Campus_Id', 'Awarded', 'Forms_Received')

    column_filters = ('Grant_Id', 'Program_Id', 'Student_Id', 'Payment_Id', 'University_Id', 'Campus_Id', 'Awarded', 'Forms_Received')
    

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class MyAdminIndexView(AdminIndexView):
    """Custom view for index. Login secured."""
    def is_visible(self):
        # This view won't appear in the menu structure
        return False
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))
    @expose('/')
    def index(self):
        if not current_user.is_authenticated and current_user.is_admin:
            return redirect(url_for('auth.login'))
        return super(MyAdminIndexView, self).index()

#create tables for db

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
    Member_Status_2023 = db.Column(db.Boolean)
    Member_Status_2024 = db.Column(db.Boolean)
    Member_Status_2025 = db.Column(db.Boolean)
    Member_Status_2026 = db.Column(db.Boolean)
    Member_Status_2027 = db.Column(db.Boolean)
    Member_Status_2028 = db.Column(db.Boolean)
    Member_Status_2029 = db.Column(db.Boolean)
    Member_Status_2030 = db.Column(db.Boolean)

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


#Functions to import csv files 
def pd_access():
    # Username of your GitHub account
    username = '' 

    # Personal Access Token (PAO) from your GitHub account
    token = ''

    # Creates a re-usable session object with your creds in-built
    github_session = requests.Session()
    github_session.auth = (username, token)
    return github_session



def pd_download(file_name,token, github_session,converters_columns=None):
    github_session = pd_access()
    url = "https://raw.githubusercontent.com/WeidongChen1026/NCP_group_37/database/{}.csv?token={}".format(file_name, token)# Make sure the url is the raw version of the file on GitHub
    download = github_session.get(url).content
    # Reading the downloaded content and making it a pandas dataframe
    df = pd.read_csv(io.StringIO(download.decode('utf-8')), delimiter=",",converters=converters_columns)
    return df

def str2bool(v):
  return str(v).lower() in ("yes", "true", "t", "1")

def create_user():
    u = Users(Username = "testUser")
    u.set_password('testPassword')
    db.session.add(u)
    db.session.commit()

def load_pd_df_Campuses(df):
    
    for index, row in df.iterrows():
        data = Campuses(Campus_Id = row['CAMPUS_ID (PK)'],  University_Id = row['UNIVERSITY_ID (FK)'] ,Campus_Name = row['CAMPUS_NAME'] ,Campus_State = row['CAMPUS_STATE'])
        db.session.add(data)
        db.session.commit()

def load_pd_df_Grants(df):
    for index, row in df.iterrows():
        data= Grants(Grant_Id=row["GRANT_ID (PK)"], Program_Id=row["PROGRAM_ID (FK)"], Student_Id=row["STUDENT_ID (FK)"], Payment_Id=row["PAYMENT_ID (FK)"], University_Id=row["UNIVERSITY_ID (FK)"], Campus_Id=row["CAMPUS_ID (FK)"], Awarded=str2bool(row["AWARDED"]), Forms_Received=str2bool(row["FORMS_RECEIVED"]))
        db.session.add(data)
        db.session.commit()  

def load_pd_df_Universities(df):
    for index, row in df.iterrows():
        data = Universities(University_Id =row['UNIVERSITY_ID (PK)'], University_Name = row['UNIVERSITY_NAME'], ABN=  row['ABN'], Member_Status_2014= str2bool(row["MEMBER_STATUS_2014"]), Member_Status_2015= str2bool(row["MEMBER_STATUS_2015"]), Member_Status_2016= str2bool(row["MEMBER_STATUS_2016"]), Member_Status_2017=str2bool(row["MEMBER_STATUS_2017"]),
        Member_Status_2018=str2bool(row["MEMBER_STATUS_2018"]), Member_Status_2019=str2bool(row["MEMBER_STATUS_2019"]), Member_Status_2020=str2bool(row["MEMBER_STATUS_2020"]), Member_Status_2021=str2bool(row["MEMBER_STATUS_2021"]), Member_Status_2022=str2bool(row["MEMBER_STATUS_2022"]),
        Member_Status_2023=str2bool(row["MEMBER_STATUS_2023"]), Member_Status_2024=str2bool(row["MEMBER_STATUS_2024"]), Member_Status_2025=str2bool(row["MEMBER_STATUS_2025"]), Member_Status_2026=str2bool(row["MEMBER_STATUS_2026"]), Member_Status_2027=str2bool(row["MEMBER_STATUS_2027"]),
        Member_Status_2028=str2bool(row["MEMBER_STATUS_2028"]), Member_Status_2029=str2bool(row["MEMBER_STATUS_2029"]), Member_Status_2030=str2bool(row["MEMBER_STATUS_2030"]))
        db.session.add(data)
        db.session.commit()    

def load_pd_df_Payments(df):
    for index, row in df.iterrows():
        data= Payments(Payment_Id=row["PAYMENT_ID"], Student_Id=row["STUDENT_ID (FK)"], Program_Id=row["PROGRAM_ID (FK)"], UWA_Business_Unit=row["UWA_BUSINESS_UNIT"], Payment_Date=datetime.strptime(row["PAYMENT_DATE"],'%Y-%m-%d').date(), Payment_Amount=row["PAYMENT_AMOUNT"],
        UWA_Account_Number=row["UWA_ACCOUNT_NUMBER"], Funding_Round=row["FUNDING_ROUND"], Description=row["DESCRIPTION"])
        db.session.add(data)
        db.session.commit()  

def load_pd_df_Programs(df):
    names = list(df.keys())
    for index, row in df.iterrows():
        data = Programs(Program_Id=row["PROGRAM_ID (PK)"], Program_Name=row["PROGRAM_NAME"], Program_Acronym=row["PROGRAM_ACRONYM"], Year=row["YEAR"], Class_Code=row["CLASS_CODE"], Project_Code=row["PROJECT_CODE"], ISEO_Code=row["ISEO_CODE"], UWA_Mobility_Grant_Project_Grant_Number=row["UWA_MOBILITY_GRANT_PROJECT_GRANT_NUMBER"],
        UWA_Admin_Funding_Project_Grant_Number=row["UWA_ADMIN_FUNDING_PROJECT_GRANT_NUMBER"], Program_Type=row["PROGRAM_TYPE"], Project_Status=row["PROJECT_STATUS"], Funding_Acquittal_Date=datetime.strptime(row["FUNDING_ACQUITTAL _DATE"],'%d/%m/%Y').date(), Project_Completion_Submission_Date=datetime.strptime(row["PROJECT_COMPLETION_SUBMISSION_DATE"],'%d/%m/%Y').date(),
        Project_Completion_Report_Link=row["PROJECT_COMPLETION_REPORT_LINK"], Refund_Utilisation_Commonwealth_Date=datetime.strptime(row["REFUND_UTILISATION_COMMONWEALTH_DATE"],'%d/%m/%Y').date(), Commonwealth_Refund_Invoice_Link=row["COMMONWEALTH_REFUND_INVOICE_LINK"], Statutory_Decleration_Date=datetime.strptime(row["STATUTORY_DECLORATION_DATE"],'%d/%m/%Y').date(),
        Statutory_Decleration_Link=row["STATUTORY_DECLARATION_LINK"], Original_Project_Schedule=row["ORIGINAL_PROJECT_SCHEDULE_LINK"], Deed_Of_Variation_One=row["DEED_OF_VARIATION_1_LINK"], Deed_Of_Variation_Two=row["DEED_OF_VARIATION_2_LINK"], Deed_Of_Variation_Three=row["DEED_OF_VARIATION_3_LINK"],
        Mobility_Grant_Funding_Received=row["MOBILITY_GRANT_FUNDING_RECIEVED"], Mobility_Grant_Dollar_Size=row["MOBILITY_GRANT_DOLLAR_SIZE"], Mobility_Grant_Funding_Utilised=row["MOBILITY_GRANT_FUNDING_UTILISED"], Mobility_Grant_Funding_Remaining=row["MOBILITY_GRANT_FUNDING_REMAINING"],
        Mobility_Grants_Received=row["MOBILITY_GRANTS_RECEIVED"], Mobility_Grants_Utilised=row["MOBILITY_GRANTS_UTILISED"], Mobility_Grants_Remaining=row["MOBILITY_GRANTS_UTILISED"],
        Internship_Grant_Funding_Received=row["INTERNSHIP_GRANT_FUNDING_RECIEVED"], Internship_Grant_Dollar_Size=row["INTERNSHIP_GRANT_DOLLAR_SIZE"], Internship_Grant_Funding_Utilised=row["INTERNSHIP_GRANT_FUNDING_UTILISED"], Internship_Grant_Funding_Remaining=row["INTERNSHIP_GRANT_FUNDING_REMAINING"],
        Internship_Grants_Received=row["INTERNSHIP_GRANTS_RECEIVED"], Internship_Grants_Utilised=row["INTERNSHIP_GRANTS_UTILISED"], Internship_Grants_Remaining=row["INTERNSHIP_GRANTS_REMAINING"],
        Language_Grant_Funding_Received=row["LANGUAGE_GRANT_FUNDING_RECIEVED"], Language_Grant_Dollar_Size=row["LANGUAGE_GRANT_DOLLAR_SIZE"], Language_Grant_Funding_Utilised=row['LANGUAGE_GRANT_FUNDING_UTILISED'], Language_Grant_Funding_Remaining=row["LANGUAGE_GRANT_FUNDING_REMAINING"],
        Language_Grants_Received=row["LANGUAGE_GRANTS_RECEIVED"], Language_Grants_Utilised=row["LANGUAGE_GRANTS_UTILISED"], Language_Grants_Remaining=row["LANGUAGE_GRANTS_REMAINING"],
        Administration_Grant_Funding_Received=row["ADMINISTRATION_GRANT_FUNDING_RECIEVED"], Administration_Grant_Dollar_Size=row["ADMINISTRATION_GRANT_DOLLAR_SIZE"], Administration_Grant_Funding_Utilised=row["ADMINISTRATION_GRANT_FUNDING_UTILISED"], Administration_Grant_Funding_Remaining=row["ADMINISTRATION_GRANT_FUNDING_REMAINING"],
        Administration_Grants_Received=row["ADMINISTRATION_GRANTS_RECEIVED"], Administration_Grants_Utilised=row["ADMINISTRATION_GRANTS_UTILISED"], Administration_Grants_Remaining=row["ADMINISTRATION_GRANTS_REMAINING"],
        Total_Grant_Funding_Received=row["TOTAL_GRANT_FUNDING_RECIEVED"], Total_Grant_Funding_Utilised=row["TOTAL_GRANT_FUNDING_UTILISED"], Total_Grant_Funding_Remaining=row["TOTAL_GRANT_FUNDING_REMAINING"],
        Total_Grants_Received=row["TOTAL_GRANTS_RECEIVED"], Total_Grants_Utilised=row["TOTAL_GRANTS_UTILISED"], Total_Grants_Remaining=row["TOTAL_GRANTS_REMAINING"], Notes = row["NOTES"])

        db.session.add(data)
        db.session.commit()  

def load_pd_df_Students(df):
    for index, row in df.iterrows():
        data = Students(Student_Id=row["STUDENT_ID (PK)"],University_Id = row["UNIVERSITY_ID (FK)"], Campus_Id = row["CAMPUS_ID (FK)"],Student_Number = row["STUDENT_NUMBER"],Title=row["TITLE"], First_Name=row["FIRST_NAME"], 
        Preferred_Name=row["PREFERRED_NAME"], Last_Name=row["LAST_NAME"], Address_Line_One=row["ADDRESS_LINE_1"], Address_Line_Two=row["ADDRESS_LINE_2"], City=row["CITY"], Postcode=row["POSTCODE"], State=row["STATE"], Country=row["COUNTRY"], Date_Of_Birth=datetime.strptime(row["DATE_OF_BIRTH"],'%Y-%m-%d').date(), Phone_Number=row["PHONE_NUMBER"], 
        Student_Email=row["STUDENT_EMAIL"], Gender=row["GENDER"], BSB=row["BSB"], Account_Number=row["ACCOUNT_NUMBER"], Field_Of_Study=row["FIELD_OF_STUDY_CODE"], Country_Of_Birth=row["COUNTRY_OF_BIRTH"],Indigenous_Australian= str2bool(row["INDIGENOUS_AUSTRALIAN"]), Disability= str2bool(row["DISABILITY"]), Aus_Citizen= str2bool(row["AUS_CITIZEN"]), Notes=row["NOTES"])
        db.session.add(data)
        db.session.commit()

#Dummy data uploaded. Uncoment if you need tp populate the database again. 
#github_session = pd_access()
# create_user()
# df = pd_download('CAMPUSES', '', github_session) # Make sure the url is the raw version of the file on GitHub, get the toke for the file and add as third paramater for pd_download calls
# load_pd_df_Campuses(df)

# df = pd_download('GRANTS', '', github_session)
# load_pd_df_Grants(df)

# df = pd_download('PAYMENTS','', github_session)
# load_pd_df_Payments(df)

# df = pd_download('PROGRAMS', '', github_session,{'CLASS_CODE': str,'ISEO_CODE': str,'UWA_MOBILITY_GRANT_PROJECT_GRANT_NUMBER': str,'UWA_ADMIN_FUNDING_PROJECT_GRANT_NUMBER': str})
# load_pd_df_Programs(df)

# df = pd_download('STUDENTS','', github_session,{'PHONE_NUMBER': str, 'BSB': str} )
# load_pd_df_Students(df)

# df = pd_download('UNIVERSITIES','', github_session)
# load_pd_df_Universities(df)