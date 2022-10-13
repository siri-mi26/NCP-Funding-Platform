from itertools import count
from app import db, login
from flask_admin.menu import MenuLink
from flask import url_for, request, redirect
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose, BaseView
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user, login_required
import pandas as pd
from datetime import datetime
import io
import requests
# import tablib
from sqlalchemy.orm import column_property
from sqlalchemy import VARCHAR, create_engine, select, func, or_, case #, CheckConstraint
from config import  Config    
from sqlalchemy.ext.hybrid import hybrid_property
import enum

from sqlalchemy.orm import relationship, object_session

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

class InfoView(BaseView):
    @expose('/')
    def info(self):
        return self.render('info.html')

    def is_accessible(self):
        return current_user.is_authenticated  


class StudentsModelView(ModelView):
    """Custom view for Students. Login secured."""
    list_template = 'list_templates/student_info.html'
    edit_template = 'edit_templates/student_edit.html'
    create_template = 'create_templates/student_create.html'
    details_template = 'details_templates/student_details.html'
    can_export = True 
    export_types = ['csv', 'xls']
    can_edit = True
    can_delete = True
    can_create = True
    can_view_details = True
    can_set_page_size = True
    column_default_sort = 'id'
    
    column_searchable_list = ('id', 'Student_Number', 'First_Name', 'Last_Name', 'Country', 'Gender', 'University.University_Name', 'Campus.Campus_Name')

    column_list = ('id', 'Title', 'First_Name', 'Preferred_Name', 'Last_Name', 'Student_Number', 'University.University_Name',  'Campus.Campus_Name',  
         'Address_Line_One', 'Address_Line_Two', 'City', 'Postcode', 'State', 'Country', 'Date_Of_Birth', 'Phone_Number', 
        'Student_Email', 'Gender', 'BSB', 'Account_Number', 'Field_Of_Study', 'Country_Of_Birth','Indigenous_Australian', 'Disability', 'Aus_Citizen',
        'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT', 'Notes', 'University_Id', 'Campus_Id')
    
    column_details_list = ('id', 'Title', 'First_Name', 'Preferred_Name', 'Last_Name', 'Student_Number', 'University.University_Name',  'Campus.Campus_Name',  
         'Address_Line_One', 'Address_Line_Two', 'City', 'Postcode', 'State', 'Country', 'Date_Of_Birth', 'Phone_Number', 
        'Student_Email', 'Gender', 'BSB', 'Account_Number', 'Field_Of_Study', 'Country_Of_Birth','Indigenous_Australian', 'Disability', 'Aus_Citizen',
        'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT', 'Notes', 'University_Id', 'Campus_Id')

    form_columns = ('Title', 'First_Name', 'Preferred_Name', 'Last_Name', 'Student_Number',  
         'Address_Line_One', 'Address_Line_Two', 'City', 'Postcode', 'State', 'Country', 'Date_Of_Birth', 'Phone_Number', 
        'Student_Email', 'Gender', 'BSB', 'Account_Number', 'Field_Of_Study', 'Country_Of_Birth','Indigenous_Australian', 'Disability', 'Aus_Citizen',
        'CITIZENS_PR', 'Notes', 'University_Id', 'Campus_Id')

    column_filters = ('id', 'Title', 'First_Name', 'Preferred_Name', 'Last_Name', 'Student_Number', 'University.University_Name',  'Campus.Campus_Name',  
         'Address_Line_One', 'Address_Line_Two', 'City', 'Postcode', 'State', 'Country', 'Date_Of_Birth', 'Phone_Number', 
        'Student_Email', 'Gender', 'BSB', 'Account_Number', 'Field_Of_Study', 'Country_Of_Birth','Indigenous_Australian', 'Disability', 'Aus_Citizen',
        'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT', 'Notes', 'University_Id', 'Campus_Id')

    column_sortable_list = ('id', 'Title', 'First_Name', 'Preferred_Name', 'Last_Name', 'Student_Number', 'University.University_Name',  'Campus.Campus_Name',  
         'Address_Line_One', 'Address_Line_Two', 'City', 'Postcode', 'State', 'Country', 'Date_Of_Birth', 'Phone_Number', 
        'Student_Email', 'Gender', 'BSB', 'Account_Number', 'Field_Of_Study', 'Country_Of_Birth','Indigenous_Australian', 'Disability', 'Aus_Citizen',
        'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT', 'Notes', 'University_Id', 'Campus_Id')

    column_labels = {'id': 'Student ID', 'University_Acronym': 'University Acronym', 'University_Id': 'University ID', 'Campus_Id': 'Campus ID', 'BSB': 'BSB', 'Student_Id': 'Student ID', 
        'Student_Number': 'Student Number', 'First_Name': 'First Name', 'Last_Name': 'Last Name', 'CITIZENS_PR': 'Citizen\'s PR', 'SHORT_TERM_GRANT': 'Short Term Grant', 
        'SEMESTER_GRANT': 'Semester Grant', 'University.University_Name': 'University Name',  'Campus.Campus_Name': 'Campus Name' , 'Indigenous_Australian': 'Indigenous Aus',
        'Notes': 'Extra Notes'}

    column_descriptions = {'University_Acronym': 'Related University Acronym', 'Student_Number': 'Student University Number', 
        'Title': 'Student\'s Title', 'First_Name': 'Student\'s First Name', 'Preferred_Name' : 'Student\'s Preferred Name', 'Last_Name': 'Student\'s Last Name or Surname', 
        'Address_Line_One': 'Student\'s Residential First Address Line', 'Address_Line_Two': 'Student\'s Reseidential Second Address Line (if needed)', 
        'City': 'Student\'s Residential City or Suburb', 'Postcode': 'Student\'s Residential Postcode', 'State': 'Student\'s Residential State', 'Country': 'Student\'s Residential Country', 
        'Date_Of_Birth': 'Student\'s Date of Birth', 'Phone_Number': 'Student\'s Mobile Phone Number', 'Student_Email': 'Student\'s University Email Address', 
        'Gender': 'Student\'s Identified Gender', 'BSB': 'Student\'s Bank Account BSB', 'Account_Number': 'Student\'s Bank Account Number', 
        'Field_Of_Study': 'Student\'s Designated Field of Study', 'Country_Of_Birth': 'Student\'s Country of Birth', 'Indigenous_Australian': 'Does Student identify as an Indigenous Australian?', 
        'Disability': 'Does Student identify as having a Disability?', 'Aus_Citizen': 'Is the Student an Australian Citizen?', 
        'CITIZENS_PR': 'Not previously Indonesian Citizen and/or Permanent Resident','SHORT_TERM_GRANT': 'Previously Received a Short Term Grant','SEMESTER_GRANT': 'Previously Received a Semester Grant',
        'Notes': 'Any extra notes on the Student','id': 'Unique Student ID', 'University_Id': 'University ID of University Student Attends', 'Campus_Id': 'Campus ID of Campus Student Attends', 'Campus.Campus_Name': 'Name of Campus Student Attends', 
        'University.University_Name': 'Name of University that Student Attends'}

    


    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))
    


class ProgramsModelView(ModelView):
    """Custom view for Programs. Login secured."""
    list_template = 'list_templates/program_info.html'
    edit_template = 'edit_templates/program_edit.html'
    create_template = 'create_templates/program_create.html'
    details_template = 'details_templates/program_details.html'
    can_export = True 
    export_types = ['csv', 'xls']
    can_edit = True
    can_delete = True
    can_create = True
    can_view_details = True
    can_set_page_size = True
    column_default_sort = 'id' 

    column_searchable_list = ('id', 'Program_Name', 'Program_Acronym', 'Program_Type')

    column_list = ('id', 'Program_Name', 'Program_Acronym', 'Year', 'Class_Code', 'Project_Code', 'ISEO_Code', 'UWA_Mobility_Grant_Project_Grant_Number',
        'UWA_Admin_Funding_Project_Grant_Number', 'Program_Type',  'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT','Funding_Acquittal_Date', 'Project_Completion_Submission_Date',
        'Project_Completion_Report_Link', 'Refund_Utilisation_Commonwealth_Date', 'Commonwealth_Refund_Invoice_Link', 'Statutory_Decleration_Date',
        'Statutory_Decleration_Link', 'Original_Project_Schedule', 'Deed_Of_Variation_One', 'Deed_Of_Variation_Two', 'Deed_Of_Variation_Three', 'Notes')
#'Project_Status',
    column_details_list = ('id', 'Program_Name', 'Program_Acronym', 'Year', 'Class_Code', 'Project_Code', 'ISEO_Code', 'UWA_Mobility_Grant_Project_Grant_Number',
        'UWA_Admin_Funding_Project_Grant_Number', 'Program_Type', 'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT','Funding_Acquittal_Date', 'Project_Completion_Submission_Date',
        'Project_Completion_Report_Link', 'Refund_Utilisation_Commonwealth_Date', 'Commonwealth_Refund_Invoice_Link', 'Statutory_Decleration_Date',
        'Statutory_Decleration_Link', 'Original_Project_Schedule', 'Deed_Of_Variation_One', 'Deed_Of_Variation_Two', 'Deed_Of_Variation_Three', 'Notes')


    form_columns = ('Program_Name', 'Program_Acronym', 'Year', 'Class_Code', 'Project_Code', 'ISEO_Code', 'UWA_Mobility_Grant_Project_Grant_Number',
        'UWA_Admin_Funding_Project_Grant_Number', 'Program_Type',  'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT', 'Funding_Acquittal_Date', 'Project_Completion_Submission_Date',
        'Project_Completion_Report_Link', 'Refund_Utilisation_Commonwealth_Date', 'Commonwealth_Refund_Invoice_Link', 'Statutory_Decleration_Date',
        'Statutory_Decleration_Link', 'Original_Project_Schedule', 'Deed_Of_Variation_One', 'Deed_Of_Variation_Two', 'Deed_Of_Variation_Three', 'Notes')

    
    column_filters = ('id', 'Program_Name', 'Program_Acronym', 'Year', 'Class_Code', 'Project_Code', 'ISEO_Code', 'UWA_Mobility_Grant_Project_Grant_Number',
        'UWA_Admin_Funding_Project_Grant_Number', 'Program_Type', 'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT','Funding_Acquittal_Date', 'Project_Completion_Submission_Date',
        'Project_Completion_Report_Link', 'Refund_Utilisation_Commonwealth_Date', 'Commonwealth_Refund_Invoice_Link', 'Statutory_Decleration_Date',
        'Statutory_Decleration_Link', 'Original_Project_Schedule', 'Deed_Of_Variation_One', 'Deed_Of_Variation_Two', 'Deed_Of_Variation_Three', 'Notes')

    column_sortable_list= ('id', 'Program_Name', 'Program_Acronym', 'Year', 'Class_Code', 'Project_Code', 'ISEO_Code', 'UWA_Mobility_Grant_Project_Grant_Number',
        'UWA_Admin_Funding_Project_Grant_Number', 'Program_Type', 'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT','Funding_Acquittal_Date', 'Project_Completion_Submission_Date',
        'Project_Completion_Report_Link', 'Refund_Utilisation_Commonwealth_Date', 'Commonwealth_Refund_Invoice_Link', 'Statutory_Decleration_Date',
        'Statutory_Decleration_Link', 'Original_Project_Schedule', 'Deed_Of_Variation_One', 'Deed_Of_Variation_Two', 'Deed_Of_Variation_Three', 'Notes')

    column_labels = {'Program_Name': 'Program Name', 'Program_Acronym': 'Program Acronym', 'Year': 'Year', 'Class_Code': 'Class Code', 
        'Project_Code': 'Project Code', 'ISEO_Code': 'ISEO Code', 'UWA_Mobility_Grant_Project_Grant_Number': 'UWA Mobility Grant Project Grant Number',
        'UWA_Admin_Funding_Project_Grant_Number': 'UWA Admin Funding Project Grant Number', 'Program_Type': 'Program Type',
        'CITIZENS_PR': 'Citizen\'s PR', 'SHORT_TERM_GRANT': 'Short Term Grant', 'SEMESTER_GRANT': 'Semester Grant', 'Funding_Acquittal_Date': 'Funding Acquittal Date', 
        'Project_Completion_Submission_Date': 'Project Completion Submission Date', 'Project_Completion_Report_Link': 'Project Completion Report Link', 
        'Refund_Utilisation_Commonwealth_Date': 'Refund Utilisation Commonwealth Date', 'Commonwealth_Refund_Invoice_Link': 'Commonwealth Refund Invoice Link', 
        'Statutory_Decleration_Date': 'Statutory Decleration Date','Statutory_Decleration_Link': 'Statutory Decleration Link', 'Original_Project_Schedule': 'Original Project Schedule', 
        'Deed_Of_Variation_One': 'Deed Of Variation One', 'Deed_Of_Variation_Two': 'Deed Of Variation Two', 'Deed_Of_Variation_Three': 'Deed Of Variation Three', 'Notes': 'Extra Notes', 'id': 'Program ID'}

    
    column_descriptions = {'Program_Name': 'Name of Grant Program', 'Program_Acronym': 'Grant Program Acronym', 'Year': 'Year Of Program', 'Class_Code': 'Class Code Of Program',
        'Project_Code': 'Class Code Of Project', 'ISEO_Code': 'ISEO Code Of Program', 'UWA_Mobility_Grant_Project_Grant_Number': 'Unique Code Set Up For Each Year’s NCP Mobility Grant Funding Allocations', 
        'UWA_Admin_Funding_Project_Grant_Number': 'Unique Code Set Up For Each Year’s NCP Admin Grant Funding Allocations', 'Program_Type': 'Type of Program - Short-Term or Semester',
        'CITIZENS_PR': 'Not previously Indonesian Citizen and/or Permanent Resident', 'SHORT_TERM_GRANT': 'Previously Received a Short Term Grant', 'SEMESTER_GRANT': 'Previously Received a Semester Grant', 
        'Funding_Acquittal_Date' : 'Due Date For The Acquittal', 'Project_Completion_Submission_Date': 'Completion Date Of Project', 'Project_Completion_Report_Link': 'Link To Project Completion Report in Dropbox',
        'Refund_Utilisation_Commonwealth_Date': 'Date Refund Is Processed ', 'Commonwealth_Refund_Invoice_Link': 'Link To Dropbox For Commonwealth Refund Invoice Link', 'Statutory_Decleration_Date': 'The Date Of The Statuatory Declaration Being Signed & Submitted', 
        'Statutory_Decleration_Link': 'Link to Dropbox For Statutory Declaration', 'Original_Project_Schedule': 'Link To Dropbox For Original Project Schedule', 'Deed_Of_Variation_One': 'Link To Dropbox For Deed of Variation One', 
        'Deed_Of_Variation_Two': 'Link To Dropbox For Deed of Variation Two', 'Deed_Of_Variation_Three': 'Link To Dropbox For Deed of Variation Three', 'Notes': 'Any Extra Notes On The Program', 'id': 'Unique Program ID'}
    
    # actor_table  = db.select(db.Programs.c.Mobility_Grants_Utilised)
    session = db.Session()
    


    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class UniversitiesModelView(ModelView):
    """Custom view for University. Login secured."""
    list_template = 'list_templates/universityinfo_info.html'
    edit_template = 'edit_templates/universityinfo_edit.html'
    create_template = 'create_templates/universityinfo_create.html'
    details_template = 'details_templates/universityinfo_details.html'
    can_export = True 
    export_types = ['csv', 'xls']
    can_edit = True
    can_delete = True
    can_create = True
    can_view_details = True
    can_set_page_size = True
    column_default_sort = 'id' 

    column_searchable_list = ('id', 'University_Acronym', 'University_Name')

    column_list =  ('id', 'University_Acronym', 'University_Name', 'ABN')

    column_details_list = ('id', 'University_Acronym', 'University_Name', 'ABN')

    form_columns =  ('University_Acronym', 'University_Name', 'ABN')

    column_filters = ('id', 'University_Acronym', 'University_Name', 'ABN')

    column_sortable_list = ('id', 'University_Acronym', 'University_Name', 'ABN')

    column_labels = {'ABN': 'ABN', 'University_Acronym': 'University Acronym', 'id': 'University ID', 'University_Name': 'University Name'}

    column_descriptions = {'id': 'Unique University ID', 'University_Acronym': 'Acronym for University' , 'University_Name': 'Name Of Each University', 'ABN': 'ABN Number Of Each University'}

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class CampusesModelView(ModelView):
    """Custom view for Campuses. Login secured."""
    list_template = 'list_templates/campus_info.html'
    edit_template = 'edit_templates/campus_edit.html'
    create_template = 'create_templates/campus_create.html'
    details_template = 'details_templates/campus_details.html'
    can_export = True 
    export_types = ['csv', 'xls']
    can_edit = True
    can_delete = True
    can_create = True
    can_view_details = True
    can_set_page_size = True
    column_default_sort = 'id'

    column_searchable_list = ('id', 'Campus_Name', 'University.University_Name', 'University.University_Acronym', 'University_Id')

    column_list = ('id', 'Campus_Name', 'University.University_Name', 'University.University_Acronym', 'Campus_State', 'University_Id')

    column_details_list = ('id', 'Campus_Name', 'University.University_Name', 'University.University_Acronym', 'Campus_State', 'University_Id')

    form_columns = ('Campus_Name', 'Campus_State', 'University_Id')

    column_filters = ('id', 'Campus_Name', 'University.University_Name', 'University.University_Acronym', 'Campus_State', 'University_Id')
    
    column_sortable_list = ('id', 'Campus_Name', 'University.University_Name', 'University.University_Acronym', 'Campus_State', 'University_Id')
       
    column_labels = {'University.University_Acronym': 'University Acronym', 'University.University_Name': 'University Name','id': 'Campus ID', 
        'University_Id': 'University ID', 'Campus_Name': 'Campus Name'}

    column_descriptions = {'University.University_Acronym': 'Related University Acronym', 'University.University_Name': 'Related University Name', 
    'Campus_Name': 'Name of Campus', 'Campus_State': 'State Campus is Located', 'id': 'Unique Campus ID', 'University_Id': 'Related University ID', }

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class PaymentsModelView(ModelView):
    """Custom view for Payments. Login secured."""
    list_template = 'list_templates/payment_info.html'
    edit_template = 'edit_templates/payment_edit.html'
    create_template = 'create_templates/payment_create.html'
    details_template = 'details_templates/payment_details.html'
    can_export = True 
    export_types = ['csv', 'xls']
    can_edit = True
    can_delete = True
    can_create = True
    can_view_details = True
    can_set_page_size = True
    column_default_sort = 'id'

    column_searchable_list = ('id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 
        'Payment_Amount', 'Funding_Round', 'Student_Id', 'Program_Id')

    column_list = ('id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'UWA_Business_Unit', 
        'Payment_Date', 'Payment_Amount', 'UWA_Account_Number', 'Funding_Round', 'Description', 'Student_Id', 'Program_Id')

    column_details_list = ('id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'UWA_Business_Unit', 
        'Payment_Date', 'Payment_Amount', 'UWA_Account_Number', 'Funding_Round', 'Description', 'Student_Id', 'Program_Id')

    form_columns = ('UWA_Business_Unit', 'Payment_Date', 'Payment_Amount', 'UWA_Account_Number', 'Funding_Round', 'Description', 'Student_Id', 'Program_Id')

    column_filters = ('id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'UWA_Business_Unit', 
        'Payment_Date', 'Payment_Amount', 'UWA_Account_Number', 'Funding_Round', 'Description', 'Student_Id', 'Program_Id')

    column_sortable_list  = ('id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'UWA_Business_Unit', 
        'Payment_Date', 'Payment_Amount', 'UWA_Account_Number', 'Funding_Round', 'Description', 'Student_Id', 'Program_Id')

    column_labels = {'UWA_Business_Unit': 'UWA Business Unit', 'UWA_Account_Number': 'UWA Account Number', 'id': 'Payment ID', 
        'Student.First_Name': 'Student First Name', 'Student.Last_Name': 'Student Last Name', 
        'Program.Program_Name': 'Program Name', 'Program.Year': 'Program Year', 'Payment_Amount': 'Payment Amount',
        'Funding_Round': 'Funding Round', 'Student_Id': 'Student ID', 'Program_Id': 'Program ID', 'id': 'Payment ID'}

    column_descriptions = {'id': 'Unique Payment ID', 'Student.First_Name': 'Related Student\'s First Name', 'Student.Last_Name': 'Related Student\'s Last Name', 
        'Program.Program_Name': 'Related Program\'s Name', 'Program.Year': 'Related Program\'s Year', 'UWA_Business_Unit': 'UWA Global Learning Business Unit', 
        'Payment_Date': 'Date of Payment to Student', 'Payment_Amount': 'Amount Paid to Student', 'UWA_Account_Number': 'ACICIS Account Number', 
        'Funding_Round': 'Funding Round Payment Is From', 'Description': 'Summary Description of Payment Details', 'Student_Id': 'Related Student ID', 'Program_Id': 'Related Program ID'} 

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class GrantsModelView(ModelView):
    """Custom view for Grants. Login secured."""
    list_template = 'list_templates/grant_info.html'
    edit_template = 'edit_templates/grant_edit.html'
    create_template = 'create_templates/grant_create.html'
    details_template = 'details_templates/grant_details.html'
    can_export = True 
    export_types = ['csv', 'xls']
    can_edit = True
    can_delete = True
    can_create = True
    can_view_details = True
    can_set_page_size = True
    column_default_sort = 'id' 

    column_searchable_list = ('id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'Payment.Payment_Amount', 'University.University_Name', 
        'Campus.Campus_Name', 'Period', 'Year_Undertaken', 'Program.Program_Type', 'Student_Id', 'Program_Id', 'Payment_Id', 'University_Id', 'Campus_Id', 'Grant_Type')
    
    column_list = ('id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'Payment.Payment_Amount', 'University.University_Name', 
        'Campus.Campus_Name', 'Start_Date', 'End_Date', 'Period', 'Year_Undertaken', 'Program.Program_Type', 'Grant_Type', 'Awarded', 'Forms_Received', 'Student_Id', 'Program_Id', 'Payment_Id', 'University_Id', 'Campus_Id')
    
    column_details_list = ('id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'Payment.Payment_Amount', 'University.University_Name', 
        'Campus.Campus_Name', 'Start_Date', 'End_Date', 'Period', 'Year_Undertaken', 'Program.Program_Type', 'Grant_Type', 'Awarded', 'Forms_Received', 'Student_Id', 'Program_Id', 'Payment_Id', 'University_Id', 'Campus_Id')
    
    form_columns = ('Start_Date', 'End_Date', 'Period', 'Year_Undertaken', 'Grant_Type', 'Awarded', 'Forms_Received', 'Student_Id', 'Program_Id', 'Payment_Id', 'University_Id', 'Campus_Id')
    
    column_filters = ('id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'Payment.Payment_Amount', 'University.University_Name', 
        'Campus.Campus_Name', 'Start_Date', 'End_Date', 'Period', 'Year_Undertaken', 'Program.Program_Type', 'Grant_Type', 'Awarded', 'Forms_Received', 'Student_Id', 'Program_Id', 'Payment_Id', 'University_Id', 'Campus_Id')
    
    column_sortable_list = ('id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'Payment.Payment_Amount', 'University.University_Name', 
        'Campus.Campus_Name', 'Start_Date', 'End_Date', 'Period', 'Year_Undertaken', 'Program.Program_Type', 'Grant_Type', 'Awarded', 'Forms_Received', 'Student_Id', 'Program_Id', 'Payment_Id', 'University_Id', 'Campus_Id')
    
    column_labels = {'id': 'Grant ID', 'Student.First_Name': 'Student First Name', 'Student.Last_Name': 'Student Last Name', 'Program.Program_Name': 'Program Name', 
        'Program.Year': 'Program Year', 'Payment.Payment_Amount': 'Payment Amount', 'University.University_Name': 'University Name', 
        'Campus.Campus_Name': 'Campus Name', 'Start_Date': 'Start Date', 'End_Date': 'End Date', 'Period': 'Period', 'Program.Program_Type': 'Program Type', 'Awarded': 'Awarded',
        'Forms_Received': 'Forms Received', 'Student_Id': 'Student ID', 'Program_Id': 'Program ID', 'Payment_Id': 'Payment ID', 
        'University_Id': 'University ID', 'Campus_Id': 'Campus ID', 'Grant_Type':'Grant Type', 'Year_Undertaken':'Year Undertaken'}

    column_descriptions = {'id': 'Unique Grant ID', 'Student.First_Name': 'Related Student\'s First Name', 'Student.Last_Name': 'Related Student\'s Last Name', 'Program.Program_Name': 'Related Program\'s Name', 
        'Program.Year': 'Related Program\'s Year', 'Payment.Payment_Amount': 'Related Payment Amount', 'University.University_Name': 'Related University\'s Name', 
        'Campus.Campus_Name': 'Related Campus\' Name', 'Start_Date': 'Study Start Date', 'End_Date': 'Study End Date', 'Period': 'Study Period', 'Program.Program_Type': 'Program Type (Short-Term or Semester)', 'Awarded': 'Program Awarded to Student',
        'Forms_Received': 'Forms Received for Grant to be Processed', 'Student_Id': 'Related Student ID', 'Program_Id': 'Related Program ID', 'Payment_Id': 'Related Payment ID', 
        'University_Id': 'Related University ID', 'Campus_Id': 'Related Campus ID','Grant_Type': "Type of Grant", 'Year_Undertaken': 'Year Student Undertook Program'}

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class UniversitiesFundingModelView(ModelView):
    """Custom view for University Funding Info. Login secured."""
    # list_template = 'list_templates/universityinfo_info.html'
    # edit_template = 'edit_templates/universityinfo_edit.html'
    # create_template = 'create_templates/universityinfo_create.html'
    # details_template = 'details_templates/universityinfo_details.html'
    can_export = True 
    export_types = ['csv', 'xls']
    can_edit = True
    can_delete = True
    can_create = True
    can_view_details = True
    can_set_page_size = True
    column_default_sort = 'id' 

    column_searchable_list = ('id', 'University.University_Name', 'University_Id')

    column_list =  ('id', 'University.University_Name', 'Allocation_Year', 'Member_Status', 'Funding_Remaining', 'Grants_Remaining', 'Funding_Allocated', 'Grants_Allocated', 'University_Id')

    column_details_list = ('id', 'University.University_Name', 'Allocation_Year', 'Member_Status', 'Funding_Remaining', 'Grants_Remaining', 'Funding_Allocated', 'Grants_Allocated', 'University_Id')

    form_columns =  ('Allocation_Year', 'University_Id', 'Member_Status')

    column_filters = ('id', 'University.University_Name', 'Allocation_Year', 'Member_Status', 'Funding_Remaining', 'Grants_Remaining', 'Funding_Allocated', 'Grants_Allocated', 'University_Id')

    column_sortable_list = ('id', 'University.University_Name', 'Allocation_Year', 'Member_Status', 'Funding_Remaining', 'Grants_Remaining', 'Funding_Allocated', 'Grants_Allocated', 'University_Id')

    column_labels = {'University.University_Name': 'University Name', 'id': 'University Funding ID', 'Allocation_Year': 'Allocation Year', 'Funding_Remaining': 'Funding Remaining', 
        'Grants_Remaining': 'Grants Remaining', 'Funding_Allocated': 'Funding Allocated', 'Grants_Allocated': 'Grants Allocated', 'University_Id': 'University ID', 'Member_Status': 'Member Status'}

    column_descriptions = {'University.University_Name': 'Name of University', 'id': 'Unique University Funding ID', 'Allocation_Year': 'Allocation Year of Funding', 'Funding_Remaining': 'Total Funding Remaining for University for Year', 
        'Grants_Remaining': 'Grants Remaining for University for Year', 'Funding_Allocated': 'Funding Allocated for University for Year', 'Grants_Allocated': 'Grants ALlocated for University for Year', 'University_Id': 'Related Unique University ID', 'Member_Status': 'Member Status of University for Year'}

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class ProgramsByUniversityModelView(ModelView):
    """Custom view for Programs by University. Login secured."""
    list_template = 'list_templates/pbu_info.html'
    edit_template = 'edit_templates/pbu_edit.html'
    create_template = 'create_templates/pbu_create.html'
    details_template = 'details_templates/pbu_details.html'
    can_export = True 
    export_types = ['csv', 'xls']
    can_edit = True
    can_delete = True
    can_create = True
    can_view_details = True
    can_set_page_size = True
    column_default_sort = 'id' 

    column_searchable_list = ('id', 'University.University_Name', 'Program.Program_Name', 'Program.Year', 'Program_Id', 'University_Id')
    
    column_list = ('id', 'Allocation_Year', 'University.University_Name', 'Program.Program_Name', 'Program.Year',
        'Grant_Type', 'Grant_Dollar_Size', 'Grants_Allocated', 'Funding_Allocated', 'Grants_Utilised', 'Funding_Utilised', 'Grants_Remaining', 
        'Funding_Remaining', 'Program.Funding_Acquittal_Date', 'Program.Project_Completion_Submission_Date', 'Program_Id', 'University_Id')
        
    
    column_details_list = ('id', 'Allocation_Year', 'University.University_Name', 'Program.Program_Name', 'Program.Year',
        'Grant_Type', 'Grant_Dollar_Size', 'Grants_Allocated', 'Funding_Allocated', 'Grants_Utilised', 'Funding_Utilised', 'Grants_Remaining', 
        'Funding_Remaining', 'Program.Funding_Acquittal_Date', 'Program.Project_Completion_Submission_Date', 'Program_Id', 'University_Id')
    
    form_columns = ('Grants_Allocated', 'Grant_Dollar_Size', 'Program_Id', 'University_Id', 'Allocation_Year', 'Grant_Type')
    
    column_filters = ('id', 'Allocation_Year', 'University.University_Name', 'Program.Program_Name', 'Program.Year',
        'Grant_Type', 'Grant_Dollar_Size', 'Grants_Allocated', 'Funding_Allocated', 'Grants_Utilised', 'Funding_Utilised', 'Grants_Remaining', 
        'Funding_Remaining', 'Program.Funding_Acquittal_Date', 'Program.Project_Completion_Submission_Date', 'Program_Id', 'University_Id')
    
    column_sortable_list = ('id', 'Allocation_Year', 'University.University_Name', 'Program.Program_Name', 'Program.Year',
        'Grant_Type', 'Grant_Dollar_Size', 'Grants_Allocated', 'Funding_Allocated', 'Grants_Utilised', 'Funding_Utilised', 'Grants_Remaining', 
        'Funding_Remaining', 'Program.Funding_Acquittal_Date', 'Program.Project_Completion_Submission_Date', 'Program_Id', 'University_Id')
    
    column_labels = {'id': 'PBU ID', 'Allocation_Year': 'Allocation Year', 'University.University_Name': 'University Name', 
        'Program.Program_Name': 'Program Name', 'Program.Year': 'Program Year', 'Grant_Type': 'Grant Type', 'Grants_Allocated': 'Grants Allocated', 
        'Funding_Allocated': 'Funding Allocated', 'Program.Funding_Acquittal_Date': 'Funding Acquittal Date',
        'Program.Project_Completion_Submission_Date': 'Project Completion Date', 'Program_Id': 'Program ID', 'University_Id': 'University ID', 'Grant_Dollar_Size': 'Grant Dollar Size',
        'Grants_Utilised': 'Grants Utilised', 'Funding_Utilised': 'Funding Utilised', 'Grants_Remaining': 'Grants Remaining', 'Funding_Remaining': 'Funding Remaining'}
        
    column_descriptions = {'id': 'Unique Program by University ID', 'Allocation_Year': 'Year of Allocation of Program Funding', 'University.University_Name': 'Name of University', 
        'Program.Program_Name': 'Name of Program', 'Program.Year': 'Year of Program Funding Received from Government', 'Grant_Type': 'Grant Type (Mobility, Internship or Langauge)', 'Grants_Allocated': 'Number of Grants Allocated to the University in this Year for this Program and of this Type', 
        'Funding_Allocated': 'Total Funding Allocated to the University in this Year for this Program and of this Type', 'Programs.Funding_Acquittal_Date': 'Due Date For The Acquittal',
        'Program.Project_Completion_Submission_Date': 'Date of Project Completion', 'Program_Id': 'Related Unique Program ID', 'University_Id': 'Related Unique University ID', 'Grant_Dollar_Size': 'Dollar Size of Grant',
        'Grants_Utilised': 'Number of Grants Utilised to the University in this Year for this Program and of this Type', 'Funding_Utilised': 'Funding Utilised by this University in this Year for this Program and of this Type', 
        'Grants_Remaining': 'Number of Grants Remaining to the University in this Year for this Program and of this Type', 'Funding_Remaining': 'Funding Remaining to the University in this Year for this Program and of this Type'}

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
class GrantType(enum.Enum):
    Mobility = "Mobility"
    Language = "Language"
    Internship = "Internship"

class State(enum.Enum):
    WA = "WA"
    QLD = "QLD"
    NT = "NT"
    NSW = "NSW"
    SA = "SA"
    TAS = "TAS"


class Universities(db.Model):  
    __tablename__ = 'UNIVERSITIES' 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    University_Acronym = db.Column(db.String(120), nullable = False)
    University_Name = db.Column(db.String(100), nullable = False)
    ABN = db.Column(db.Integer)

    def __repr__(self):
        return '<University: {}>'.format(self.id, self.University_Name)


class UniversitiesFunding(db.Model):
    __tablename__ = 'UNIVERSITIESFUNDING' 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    University_Id = db.Column(db.String(50), db.ForeignKey('UNIVERSITIES.id'), nullable = False)
    Allocation_Year = db.Column(db.Integer)
    Member_Status = db.Column(db.Boolean)

#looks for funding allocated for university - sum across PBU for university and year
    @hybrid_property
    def Funding_Allocated(self):
        return object_session(self).query(ProgramsByUniversity).filter((ProgramsByUniversity.University_Id == self.University_Id) & (ProgramsByUniversity.Allocation_Year == self.Allocation_Year)).count()
    @Funding_Allocated.expression
    def Funding_Allocated(cls):
        return select([func.count(ProgramsByUniversity.Funding_Allocated)]).where((ProgramsByUniversity.University_Id == cls.University_Id) & (ProgramsByUniversity.Allocation_Year == cls.Allocation_Year)).scalar_subquery()

    @hybrid_property
    def Grants_Allocated(self):
        return object_session(self).query(ProgramsByUniversity).filter((ProgramsByUniversity.University_Id == self.University_Id) & (ProgramsByUniversity.Allocation_Year == self.Allocation_Year)).count()
    @Grants_Allocated.expression
    def Grants_Allocated(cls):
        return select([func.count(ProgramsByUniversity.Funding_Allocated)]).where((ProgramsByUniversity.University_Id == cls.University_Id) & (ProgramsByUniversity.Allocation_Year == cls.Allocation_Year)).scalar_subquery()

    @hybrid_property
    def Funding_Remaining(self):
        return object_session(self).query(ProgramsByUniversity).filter((ProgramsByUniversity.University_Id == self.University_Id) & (ProgramsByUniversity.Allocation_Year == self.Allocation_Year)).count()
    @Funding_Remaining.expression
    def Funding_Remaining(cls):
        return select([func.count(ProgramsByUniversity.Funding_Allocated)]).where((ProgramsByUniversity.University_Id == cls.University_Id) & (ProgramsByUniversity.Allocation_Year == cls.Allocation_Year)).scalar_subquery()

    @hybrid_property
    def Grants_Remaining(self):
        return object_session(self).query(ProgramsByUniversity).filter((ProgramsByUniversity.University_Id == self.University_Id) & (ProgramsByUniversity.Allocation_Year == self.Allocation_Year)).count()
    @Grants_Remaining.expression
    def Grants_Remaining(cls):
        return select([func.count(ProgramsByUniversity.Funding_Allocated)]).where((ProgramsByUniversity.University_Id == cls.University_Id) & (ProgramsByUniversity.Allocation_Year == cls.Allocation_Year)).scalar_subquery()

# NOTES
# return object_session(self).query(Grants, Programs).filter((Grants.Student_Id == self.id) & (Grants.Program_Id == Programs.id) & (Programs.Program_Type.like('%Semester%'))).count()
# return select([func.count(Grants.id)]).where((Grants.Student_Id == cls.id) & (Grants.Program_Id == Programs.id) & (Programs.Program_Type.like('%Semester%'))).scalar_subquery()
    University = db.relationship(Universities, backref=db.backref('UNIVERSITIESFUNDING', uselist=True, lazy='select'))


class Campuses(db.Model):  
    __tablename__ = 'CAMPUSES' 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    University_Id = db.Column(db.String(50), db.ForeignKey('UNIVERSITIES.id'), nullable = False)
    Campus_Name = db.Column(db.String(50), nullable = False)
    Campus_State = db.Column(db.Enum(State))

    University = db.relationship(Universities, backref=db.backref('CAMPUSES', uselist=True, lazy='select'))

    def __repr__(self):
        return '<Campus: {}>'.format(self.id, self.Campus_Name)


class Students(db.Model):  
    __tablename__ = 'STUDENTS' 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    University_Id =  db.Column(db.String(50), db.ForeignKey('UNIVERSITIES.id'), nullable = False)
    Campus_Id =  db.Column(db.String(50), db.ForeignKey('CAMPUSES.id'), nullable = False)
    Student_Number = db.Column(db.Integer, nullable = False) #db.CheckConstraint('Student_Number > 10'), (before nullable)
    Title = db.Column(db.String(50))
    First_Name = db.Column(db.String(50), nullable = False)
    Preferred_Name = db.Column(db.String(50))
    Last_Name = db.Column(db.String(50), nullable = False)
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
    CITIZENS_PR = db.Column(db.Boolean)

    @hybrid_property
    def SHORT_TERM_GRANT(self):
        return object_session(self).query(Grants, Programs).filter((Grants.Student_Id == self.id) & (Grants.Program_Id == Programs.id) & (Programs.Program_Type.like('%Short Term%'))).count()
    @SHORT_TERM_GRANT.expression
    def SHORT_TERM_GRANT(cls):
        return select([func.count(Grants.id)]).where((Grants.Student_Id == cls.id) & (Grants.Program_Id == Programs.id) & (Programs.Program_Type.like('%Short Term%'))).scalar_subquery()

    @hybrid_property
    def SEMESTER_GRANT(self):
        return object_session(self).query(Grants, Programs).filter((Grants.Student_Id == self.id) & (Grants.Program_Id == Programs.id) & (Programs.Program_Type.like('%Semester%'))).count()
    @SEMESTER_GRANT.expression
    def SEMESTER_GRANT(cls):
        return select([func.count(Grants.id)]).where((Grants.Student_Id == cls.id) & (Grants.Program_Id == Programs.id) & (Programs.Program_Type.like('%Semester%'))).scalar_subquery()
    Notes = db.Column(db.String(100))

    University = db.relationship(Universities, backref=db.backref('STUDENTS', uselist=True, lazy='select'))
    Campus = db.relationship(Campuses, backref=db.backref('STUDENTS', uselist=True, lazy='select'))
    
    def __repr__(self):
        return '<Student {}>'.format(self.id, self.First_Name, self.Last_Name)


class Programs(db.Model):  
    __tablename__ = 'PROGRAMS' 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    Program_Name = db.Column(db.String(100), nullable = False)
    Program_Acronym = db.Column(db.String(50), nullable = False)
    Year = db.Column(db.Integer, nullable = False)
    Class_Code = db.Column(db.String(50), unique = True)
    Project_Code = db.Column(db.String(50), unique = True)
    ISEO_Code = db.Column(db.String(50), nullable = False, unique = True)
    UWA_Mobility_Grant_Project_Grant_Number = db.Column(db.String(50))
    UWA_Admin_Funding_Project_Grant_Number = db.Column(db.String(50))
    Program_Type = db.Column(db.String(50), nullable = False)
    #Project_Status = db.Column(db.String(50)) ### should be hybrid property that changes if total funding remaining = 0
    #in previous commit before 13/10

    CITIZENS_PR = db.Column(db.Boolean)
    SHORT_TERM_GRANT = db.Column(db.Boolean)
    SEMESTER_GRANT = db.Column(db.Boolean)

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

    Notes = db.Column(db.String)


class Payments(db.Model):  
    __tablename__ = 'PAYMENTS' 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    Student_Id = db.Column(db.Integer, db.ForeignKey('STUDENTS.id'), nullable = False)
    Program_Id = db.Column(db.Integer, db.ForeignKey('PROGRAMS.id'), nullable = False)
    UWA_Business_Unit = db.Column(db.Integer)
    Payment_Date = db.Column(db.Date)
    Payment_Amount = db.Column(db.Integer, nullable = False)
    UWA_Account_Number = db.Column(db.Integer)
    Funding_Round = db.Column(db.String(50), nullable = False)
    Description = db.Column(db.String)

    Program = db.relationship(Programs, backref=db.backref('PAYMENTS', uselist=True, lazy='select'))
    Student = db.relationship(Students, backref=db.backref('PAYMENTS', uselist=True, lazy='select'))

    def __repr__(self):
        return '<Payments: {}>'.format(self.id, self.Student_Id, self.Payment_Amount)


class Grants(db.Model):  
    __tablename__ = 'GRANTS' 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    Start_Date = db.Column(db.Date)
    End_Date = db.Column(db.Date)
    Period = db.Column(db.String(50), nullable = False)
    Year_Undertaken = db.Column(db.Integer)
    Program_Id = db.Column(db.Integer, db.ForeignKey("PROGRAMS.id"), nullable = False)
    Student_Id = db.Column(db.Integer, db.ForeignKey("STUDENTS.id"), nullable = False)
    Payment_Id = db.Column(db.Integer, db.ForeignKey("PAYMENTS.id"), nullable = False)
    University_Id = db.Column(db.Integer, db.ForeignKey("UNIVERSITIES.id"), nullable = False)
    Campus_Id = db.Column(db.Integer, db.ForeignKey("CAMPUSES.id"), nullable = False)
    Grant_Type =  db.Column(db.Enum(GrantType), nullable=False)
    Awarded = db.Column(db.Boolean)
    Forms_Received = db.Column(db.Boolean)    
    University = db.relationship(Universities, backref=db.backref('GRANTS', uselist=True, lazy='select'))
    Program = db.relationship(Programs, backref=db.backref('GRANTS', uselist=True, lazy='select'))
    Student = db.relationship(Students, backref=db.backref('GRANTS', uselist=True, lazy='select'))
    Campus = db.relationship(Campuses, backref=db.backref('GRANTS', uselist=True, lazy='select'))
    Payment = db.relationship(Payments, backref=db.backref('GRANTS', uselist=True, lazy='select'))
    
    def __repr__(self):
        return '<Grant {} {} {}>'.format(self.id, self.Program_Id, self.Student_Id)  


class ProgramsByUniversity(db.Model):
    __tablename__ = 'PROGRAMSBYUNIVERSITY' 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    Allocation_Year = db.Column(db.Integer)
    Grant_Dollar_Size = db.Column(db.Integer, default = 0)
    Grants_Allocated = db.Column(db.Integer, default = 0)
    Grant_Type = db.Column(db.Enum(GrantType), nullable = False)
    Program_Id = db.Column(db.Integer, db.ForeignKey("PROGRAMS.id"), nullable = False)
    University_Id = db.Column(db.Integer, db.ForeignKey("UNIVERSITIES.id"), nullable = False)
    University = db.relationship(Universities, backref=db.backref('PROGRAMSBYUNIVERSITY', uselist=True, lazy='select'))
    Program = db.relationship(Programs, backref=db.backref('PROGRAMSBYUNIVERSITY', uselist=True, lazy='select'))

    @hybrid_property
    def Funding_Allocated(self):
        return self.Grants_Allocated * self.Grant_Dollar_Size

    @hybrid_property
    def Grants_Utilised(self):
        return object_session(self).query(Grants).filter((Grants.Program_Id == self.Program_Id) & (Grants.Year_Undertaken == self.Allocation_Year) & (Grants.University_Id == self.University_Id)).count()
    @Grants_Utilised.expression
    def Grants_Utilised(cls):
        return select([func.count(Grants.id)]).where((Grants.Program_Id == cls.Program_Id) & (Grants.Year_Undertaken == cls.Allocation_Year) & (Grants.University_Id == cls.University_Id)).scalar_subquery()

    @hybrid_property
    def Funding_Utilised(self):
        return self.Grants_Utilised * self.Grant_Dollar_Size
    
    @hybrid_property
    def Grants_Remaining(self):
        return self.Grants_Allocated - self.Grants_Utilised

    @hybrid_property
    def Funding_Remaining(self):
        return self.Funding_Allocated - self.Funding_Utilised

    # @hybrid_property
    # def Funding_Allocated(self):
    #     return self.Grants_Allocated * 10
    
    # @hybrid_property
    # def Grants_Utilised(self):
    #     return self.Grants_Allocated * 10
    
    # @hybrid_property
    # def Funding_Utilised(self):
    #     return self.Grants_Allocated * 10

    # @hybrid_property
    # def Grants_Remaining(self):
    #     return self.Grants_Allocated * 10

    # @hybrid_property
    # def Funding_Remaining(self):
    #     return self.Grants_Allocated * 10
    

    




#Functions to import csv files from github
def pd_access():
    # Username of your GitHub account
    username = '' 

    # Personal Access Token (PAO) from your GitHub account
    token = ''

    # Creates a re-usable session object with your creds in-built
    github_session = requests.Session()
    github_session.auth = (username, token)
    return github_session

###############
## function to download files two ways
###############

def pd_download(file_name,token=None, github_session=None,converters_columns=None):
    if token is not None:
        github_session = pd_access()
        url = "https://raw.githubusercontent.com/WeidongChen1026/NCP_group_37/database/{}.csv?token={}".format(file_name, token)# Make sure the url is the raw version of the file on GitHub
        download = github_session.get(url).content
        # Reading the downloaded content and making it a pandas dataframe
        df = pd.read_csv(io.StringIO(download.decode('utf-8')), delimiter=",",converters=converters_columns)
    else:
        file="../database/dummy_data/{}.csv".format(file_name)
        df = pd.read_csv(file)
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
        data = Campuses(University_Id = row['UNIVERSITY_ID (FK)'] ,Campus_Name = row['CAMPUS_NAME'] ,Campus_State = row['CAMPUS_STATE'])
        db.session.add(data)
        db.session.commit()

def load_pd_df_Grants(df):
    for index, row in df.iterrows():
        data= Grants(Start_Date=datetime.strptime(row["START_DATE"],'%d/%m/%Y').date(),End_Date=datetime.strptime(row["END_DATE"],'%d/%m/%Y').date(), Period = row['PERIOD'], Program_Id=row["PROGRAM_ID (FK)"], Student_Id=row["STUDENT_ID (FK)"], Payment_Id=row["PAYMENT_ID (FK)"], University_Id=row["UNIVERSITY_ID (FK)"], Campus_Id=row["CAMPUS_ID (FK)"], Grant_Type =row["GRANT_TYPE"], Awarded=str2bool(row["AWARDED"]), Forms_Received=str2bool(row["FORMS_RECEIVED"]), Year_Undertaken=row["YEAR_UNDERTAKEN"])
        db.session.add(data)
        db.session.commit()  

def load_pd_df_Universities(df):
    for index, row in df.iterrows():
        data = Universities(University_Acronym = row['UNIVERSITY_ACRONYM'],University_Name = row['UNIVERSITY_NAME'], ABN = row['ABN'])
        db.session.add(data)
        db.session.commit()    

def load_pd_df_Payments(df):
    for index, row in df.iterrows():
        data= Payments(Student_Id=row["STUDENT_ID (FK)"], Program_Id=row["PROGRAM_ID (FK)"], UWA_Business_Unit=row["UWA_BUSINESS_UNIT"], Payment_Date=datetime.strptime(row["PAYMENT_DATE"],'%d/%m/%Y').date(), Payment_Amount=row["PAYMENT_AMOUNT"],
        UWA_Account_Number=row["UWA_ACCOUNT_NUMBER"], Funding_Round=row["FUNDING_ROUND"], Description=row["DESCRIPTION"])
        db.session.add(data)
        db.session.commit()  

def load_pd_df_Programs(df):
    names = list(df.keys())
    for index, row in df.iterrows():
        data = Programs(Program_Name=row["PROGRAM_NAME"], Program_Acronym=row["PROGRAM_ACRONYM"], Year=row["YEAR"], Class_Code=row["CLASS_CODE"], Project_Code=row["PROJECT_CODE"], ISEO_Code=row["ISEO_CODE"], UWA_Mobility_Grant_Project_Grant_Number=row["UWA_MOBILITY_GRANT_PROJECT_GRANT_NUMBER"],
        UWA_Admin_Funding_Project_Grant_Number=row["UWA_ADMIN_FUNDING_PROJECT_GRANT_NUMBER"], Program_Type=row["PROGRAM_TYPE"], CITIZENS_PR=str2bool(row["CITIZENS_PR"]), SHORT_TERM_GRANT=str2bool(row["SHORT_TERM_GRANT"]), SEMESTER_GRANT=str2bool(row["SEMESTER_GRANT"]),Funding_Acquittal_Date=datetime.strptime(row["FUNDING_ACQUITTAL _DATE"],'%d/%m/%Y').date(), Project_Completion_Submission_Date=datetime.strptime(row["PROJECT_COMPLETION_SUBMISSION_DATE"],'%d/%m/%Y').date(),
        Project_Completion_Report_Link=row["PROJECT_COMPLETION_REPORT_LINK"], Refund_Utilisation_Commonwealth_Date=datetime.strptime(row["REFUND_UTILISATION_COMMONWEALTH_DATE"],'%d/%m/%Y').date(), Commonwealth_Refund_Invoice_Link=row["COMMONWEALTH_REFUND_INVOICE_LINK"], Statutory_Decleration_Date=datetime.strptime(row["STATUTORY_DECLORATION_DATE"],'%d/%m/%Y').date(),
        Statutory_Decleration_Link=row["STATUTORY_DECLARATION_LINK"], Original_Project_Schedule=row["ORIGINAL_PROJECT_SCHEDULE_LINK"], Deed_Of_Variation_One=row["DEED_OF_VARIATION_1_LINK"], Deed_Of_Variation_Two=row["DEED_OF_VARIATION_2_LINK"], Deed_Of_Variation_Three=row["DEED_OF_VARIATION_3_LINK"],
        Notes = row["NOTES"])
        db.session.add(data)
        db.session.commit()

def load_pd_df_Students(df):
    for index, row in df.iterrows():
        data = Students(University_Id = row["UNIVERSITY_ID (FK)"], Campus_Id = row["CAMPUS_ID (FK)"],Student_Number = row["STUDENT_NUMBER"],Title=row["TITLE"], First_Name=row["FIRST_NAME"], 
        Preferred_Name=row["PREFERRED_NAME"], Last_Name=row["LAST_NAME"], Address_Line_One=row["ADDRESS_LINE_1"], Address_Line_Two=row["ADDRESS_LINE_2"], City=row["CITY"], Postcode=row["POSTCODE"], State=row["STATE"], Country=row["COUNTRY"], Date_Of_Birth=datetime.strptime(row["DATE_OF_BIRTH"],'%d/%m/%Y').date(), Phone_Number=row["PHONE_NUMBER"], 
        Student_Email=row["STUDENT_EMAIL"], Gender=row["GENDER"], BSB=row["BSB"], Account_Number=row["ACCOUNT_NUMBER"], Field_Of_Study=row["FIELD_OF_STUDY_CODE"], Country_Of_Birth=row["COUNTRY_OF_BIRTH"],Indigenous_Australian= str2bool(row["INDIGENOUS_AUSTRALIAN"]), Disability= str2bool(row["DISABILITY"]), Aus_Citizen= str2bool(row["AUS_CITIZEN"]), CITIZENS_PR=str2bool(row["CITIZENS_PR"]), Notes=row["NOTES"])
        db.session.add(data)
        db.session.commit()

def load_pd_df_Allocations(df):
    for index, row in df.iterrows():
        data = ProgramsByUniversity(Grants_Allocated = row["GRANTS_ALLOCATED"], Allocation_Year = row["ALLOCATION_YEAR"], Program_Id = row["PROGRAM_ID"], University_Id = row["UNIVERSITY_ID"], Grant_Type = row["GRANT_TYPE"], Grant_Dollar_Size = row["GRANT_DOLLAR_SIZE"])
        db.session.add(data)
        db.session.commit()

def load_pd_df_UniversitiesFunding(df):
    for index, row in df.iterrows():
        data = UniversitiesFunding(Allocation_Year = row["ALLOCATION_YEAR"], University_Id = row["UNIVERSITY_ID"], Member_Status = str2bool(row["MEMBER_STATUS"]))
        db.session.add(data)
        db.session.commit()

################
### Dummy data uploaded. Uncoment if you need tp populate the database again. 
################

# github_session = pd_access()
# create_user()
# df = pd_download('CAMPUSES') # Make sure the url is the raw version of the file on GitHub, get the token for the file and add as third paramater for pd_download calls
# load_pd_df_Campuses(df)

# df = pd_download('GRANTS')
# load_pd_df_Grants(df)

# df = pd_download('PAYMENTS')
# load_pd_df_Payments(df)

# df = pd_download('PROGRAMS',None, None,{'CLASS_CODE': str,'ISEO_CODE': str,'UWA_MOBILITY_GRANT_PROJECT_GRANT_NUMBER': str,'UWA_ADMIN_FUNDING_PROJECT_GRANT_NUMBER': str})
# load_pd_df_Programs(df)

# df = pd_download('STUDENTS',None, None, {'PHONE_NUMBER': str} )
# load_pd_df_Students(df)

# df = pd_download('UNIVERSITIES')
# load_pd_df_Universities(df)

# df = pd_download('ALLOCATIONS')
# load_pd_df_Allocations(df)

# df = pd_download('UNIVERSITIESFUNDING')
# load_pd_df_UniversitiesFunding(df)


# fix up PBU and UF hybrid properties (got grants utilised working)
# and link based on slice of start date of grants
# possibly when add a grant, only add student and not campus/uni -> use relation
# summary on programs as well as by uni
# titles for all pages (html templates)