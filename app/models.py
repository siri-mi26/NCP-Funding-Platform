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
import tablib
from sqlalchemy.orm import column_property
from sqlalchemy import VARCHAR, create_engine, select, func
from config import  Config    
from sqlalchemy.ext.hybrid import hybrid_property

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
    column_default_sort = 'Student_Id'
    
    column_searchable_list = ('Student_Id', 'Student_Number', 'First_Name', 'Last_Name', 'Country', 'Gender', 'University.University_Name', 'Campus.Campus_Name')

    column_list = ('Student_Id', 'Title', 'First_Name', 'Preferred_Name', 'Last_Name', 'Student_Number', 'University.University_Name',  'Campus.Campus_Name',  
         'Address_Line_One', 'Address_Line_Two', 'City', 'Postcode', 'State', 'Country', 'Date_Of_Birth', 'Phone_Number', 
        'Student_Email', 'Gender', 'BSB', 'Account_Number', 'Field_Of_Study', 'Country_Of_Birth','Indigenous_Australian', 'Disability', 'Aus_Citizen',
        'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT', 'Notes', 'University_Id', 'Campus_Id')
    
    column_details_list = ('Student_Id', 'Title', 'First_Name', 'Preferred_Name', 'Last_Name', 'Student_Number', 'University.University_Name',  'Campus.Campus_Name',  
         'Address_Line_One', 'Address_Line_Two', 'City', 'Postcode', 'State', 'Country', 'Date_Of_Birth', 'Phone_Number', 
        'Student_Email', 'Gender', 'BSB', 'Account_Number', 'Field_Of_Study', 'Country_Of_Birth','Indigenous_Australian', 'Disability', 'Aus_Citizen',
        'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT', 'Notes', 'University_Id', 'Campus_Id')

    form_columns = ('Student_Id', 'Title', 'First_Name', 'Preferred_Name', 'Last_Name', 'Student_Number',  
         'Address_Line_One', 'Address_Line_Two', 'City', 'Postcode', 'State', 'Country', 'Date_Of_Birth', 'Phone_Number', 
        'Student_Email', 'Gender', 'BSB', 'Account_Number', 'Field_Of_Study', 'Country_Of_Birth','Indigenous_Australian', 'Disability', 'Aus_Citizen',
        'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT', 'Notes', 'University_Id', 'Campus_Id')

    column_filters = ('Student_Id', 'Title', 'First_Name', 'Preferred_Name', 'Last_Name', 'Student_Number', 'University.University_Name',  'Campus.Campus_Name',  
         'Address_Line_One', 'Address_Line_Two', 'City', 'Postcode', 'State', 'Country', 'Date_Of_Birth', 'Phone_Number', 
        'Student_Email', 'Gender', 'BSB', 'Account_Number', 'Field_Of_Study', 'Country_Of_Birth','Indigenous_Australian', 'Disability', 'Aus_Citizen',
        'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT', 'Notes', 'University_Id', 'Campus_Id')

    column_sortable_list = ('Student_Id', 'Title', 'First_Name', 'Preferred_Name', 'Last_Name', 'Student_Number', 'University.University_Name',  'Campus.Campus_Name',  
         'Address_Line_One', 'Address_Line_Two', 'City', 'Postcode', 'State', 'Country', 'Date_Of_Birth', 'Phone_Number', 
        'Student_Email', 'Gender', 'BSB', 'Account_Number', 'Field_Of_Study', 'Country_Of_Birth','Indigenous_Australian', 'Disability', 'Aus_Citizen',
        'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT', 'Notes', 'University_Id', 'Campus_Id')

    column_labels = { 'University_Acronym': 'University Acronym', 'University_Id': 'University ID', 'Campus_Id': 'Campus ID', 'BSB': 'BSB', 'Student_Id': 'Student ID', 
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
        'Notes': 'Any extra notes on the Student','Student_Id': 'Unique Student ID', 'University_Id': 'University ID of University Student Attends', 'Campus_Id': 'Campus ID of Campus Student Attends', 'Campus.Campus_Name': 'Name of Campus Student Attends', 
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
    column_default_sort = 'Program_Id' 

    column_searchable_list = ('Program_Id', 'Program_Name', 'Program_Acronym', 'Program_Type')

    column_list = ('Program_Id', 'Program_Name', 'Program_Acronym', 'Year', 'Class_Code', 'Project_Code', 'ISEO_Code', 'UWA_Mobility_Grant_Project_Grant_Number',
        'UWA_Admin_Funding_Project_Grant_Number', 'Program_Type', 'Project_Status', 'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT','Funding_Acquittal_Date', 'Project_Completion_Submission_Date',
        'Project_Completion_Report_Link', 'Refund_Utilisation_Commonwealth_Date', 'Commonwealth_Refund_Invoice_Link', 'Statutory_Decleration_Date',
        'Statutory_Decleration_Link', 'Original_Project_Schedule', 'Deed_Of_Variation_One', 'Deed_Of_Variation_Two', 'Deed_Of_Variation_Three',
        'Mobility_Grant_Funding_Received', 'Mobility_Grant_Dollar_Size', 
        'Mobility_Grant_Funding_Utilised_2', 'Mobility_Grant_Funding_Remaining_2',
        'Mobility_Grants_Received_2', 'Mobility_Grants_Remaining_2', 'Mobility_Grants_Utilised_2',
        'Internship_Grant_Funding_Received', 'Internship_Grant_Dollar_Size', 'Internship_Grant_Funding_Utilised_2', 'Internship_Grant_Funding_Remaining_2',
        'Internship_Grants_Received_2', 'Internship_Grants_Utilised_2', 'Internship_Grants_Remaining_2',
        'Language_Grant_Funding_Received', 'Language_Grant_Dollar_Size', 'Language_Grant_Funding_Utilised_2', 'Language_Grant_Funding_Remaining_2',
        'Language_Grants_Received_2', 'Language_Grants_Utilised_2', 'Language_Grants_Remaining_2',
        'Administration_Grant_Funding_Received', 'Administration_Grant_Dollar_Size', 'Administration_Grant_Funding_Utilised_2', 'Administration_Grant_Funding_Remaining_2',
        'Administration_Grants_Received_2', 'Administration_Grants_Utilised_2', 'Administration_Grants_Remaining_2',
        'Total_Grant_Funding_Received', 'Total_Grant_Funding_Utilised', 'Total_Grant_Funding_Remaining',
        'Total_Grants_Received', 'Total_Grants_Utilised', 'Total_Grants_Remaining', 'Notes')

    column_details_list = ('Program_Id', 'Program_Name', 'Program_Acronym', 'Year', 'Class_Code', 'Project_Code', 'ISEO_Code', 'UWA_Mobility_Grant_Project_Grant_Number',
        'UWA_Admin_Funding_Project_Grant_Number', 'Program_Type', 'Project_Status', 'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT','Funding_Acquittal_Date', 'Project_Completion_Submission_Date',
        'Project_Completion_Report_Link', 'Refund_Utilisation_Commonwealth_Date', 'Commonwealth_Refund_Invoice_Link', 'Statutory_Decleration_Date',
        'Statutory_Decleration_Link', 'Original_Project_Schedule', 'Deed_Of_Variation_One', 'Deed_Of_Variation_Two', 'Deed_Of_Variation_Three',
        'Mobility_Grant_Funding_Received', 'Mobility_Grant_Dollar_Size', 
        'Mobility_Grant_Funding_Utilised_2', 'Mobility_Grant_Funding_Remaining_2',
        'Mobility_Grants_Received_2', 'Mobility_Grants_Remaining_2', 'Mobility_Grants_Utilised_2',
        'Internship_Grant_Funding_Received', 'Internship_Grant_Dollar_Size', 'Internship_Grant_Funding_Utilised_2', 'Internship_Grant_Funding_Remaining_2',
        'Internship_Grants_Received_2', 'Internship_Grants_Utilised_2', 'Internship_Grants_Remaining_2',
        'Language_Grant_Funding_Received', 'Language_Grant_Dollar_Size', 'Language_Grant_Funding_Utilised_2', 'Language_Grant_Funding_Remaining_2',
        'Language_Grants_Received_2', 'Language_Grants_Utilised_2', 'Language_Grants_Remaining_2',
        'Administration_Grant_Funding_Received', 'Administration_Grant_Dollar_Size', 'Administration_Grant_Funding_Utilised_2', 'Administration_Grant_Funding_Remaining_2',
        'Administration_Grants_Received_2', 'Administration_Grants_Utilised_2', 'Administration_Grants_Remaining_2',
        'Total_Grant_Funding_Received', 'Total_Grant_Funding_Utilised', 'Total_Grant_Funding_Remaining',
        'Total_Grants_Received', 'Total_Grants_Utilised', 'Total_Grants_Remaining', 'Notes')


    form_columns = ('Program_Id', 'Program_Name', 'Program_Acronym', 'Year', 'Class_Code', 'Project_Code', 'ISEO_Code', 'UWA_Mobility_Grant_Project_Grant_Number',
        'UWA_Admin_Funding_Project_Grant_Number', 'Program_Type', 'Project_Status', 'CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT', 'Funding_Acquittal_Date', 'Project_Completion_Submission_Date',
        'Project_Completion_Report_Link', 'Refund_Utilisation_Commonwealth_Date', 'Commonwealth_Refund_Invoice_Link', 'Statutory_Decleration_Date',
        'Statutory_Decleration_Link', 'Original_Project_Schedule', 'Deed_Of_Variation_One', 'Deed_Of_Variation_Two', 'Deed_Of_Variation_Three',
        'Mobility_Grant_Funding_Received', 'Mobility_Grant_Dollar_Size', 
        'Internship_Grant_Funding_Received', 'Internship_Grant_Dollar_Size', 
        'Language_Grant_Funding_Received', 'Language_Grant_Dollar_Size', 
        'Administration_Grant_Funding_Received', 'Administration_Grant_Dollar_Size', 
        'Total_Grant_Funding_Received', 'Total_Grant_Funding_Utilised', 'Total_Grant_Funding_Remaining',
        'Total_Grants_Received', 'Total_Grants_Utilised', 'Total_Grants_Remaining', 'Notes')

    
    column_filters = ('Program_Id', 'Program_Name', 'Program_Acronym', 'Year', 'Class_Code', 'Project_Code', 'ISEO_Code', 'UWA_Mobility_Grant_Project_Grant_Number',
        'UWA_Admin_Funding_Project_Grant_Number', 'Program_Type', 'Project_Status','CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT','Funding_Acquittal_Date', 'Project_Completion_Submission_Date',
        'Project_Completion_Report_Link', 'Refund_Utilisation_Commonwealth_Date', 'Commonwealth_Refund_Invoice_Link', 'Statutory_Decleration_Date',
        'Statutory_Decleration_Link', 'Original_Project_Schedule', 'Deed_Of_Variation_One', 'Deed_Of_Variation_Two', 'Deed_Of_Variation_Three',
        'Mobility_Grant_Funding_Received', 'Mobility_Grant_Dollar_Size', 
        'Mobility_Grant_Funding_Utilised_2', 'Mobility_Grant_Funding_Remaining_2',
        'Mobility_Grants_Received_2', 'Mobility_Grants_Remaining_2', 'Mobility_Grants_Utilised_2',
        'Internship_Grant_Funding_Received', 'Internship_Grant_Dollar_Size', 'Internship_Grant_Funding_Utilised_2', 'Internship_Grant_Funding_Remaining_2',
        'Internship_Grants_Received_2', 'Internship_Grants_Utilised_2', 'Internship_Grants_Remaining_2',
        'Language_Grant_Funding_Received', 'Language_Grant_Dollar_Size', 'Language_Grant_Funding_Utilised_2', 'Language_Grant_Funding_Remaining_2',
        'Language_Grants_Received_2', 'Language_Grants_Utilised_2', 'Language_Grants_Remaining_2',
        'Administration_Grant_Funding_Received', 'Administration_Grant_Dollar_Size', 'Administration_Grant_Funding_Utilised_2', 'Administration_Grant_Funding_Remaining_2',
        'Administration_Grants_Received_2', 'Administration_Grants_Utilised_2', 'Administration_Grants_Remaining_2',
        'Total_Grant_Funding_Received', 'Total_Grant_Funding_Utilised', 'Total_Grant_Funding_Remaining',
        'Total_Grants_Received', 'Total_Grants_Utilised', 'Total_Grants_Remaining', 'Notes')

    column_sortable_list= ('Program_Id', 'Program_Name', 'Program_Acronym', 'Year', 'Class_Code', 'Project_Code', 'ISEO_Code', 'UWA_Mobility_Grant_Project_Grant_Number',
        'UWA_Admin_Funding_Project_Grant_Number', 'Program_Type', 'Project_Status','CITIZENS_PR','SHORT_TERM_GRANT','SEMESTER_GRANT','Funding_Acquittal_Date', 'Project_Completion_Submission_Date',
        'Project_Completion_Report_Link', 'Refund_Utilisation_Commonwealth_Date', 'Commonwealth_Refund_Invoice_Link', 'Statutory_Decleration_Date',
        'Statutory_Decleration_Link', 'Original_Project_Schedule', 'Deed_Of_Variation_One', 'Deed_Of_Variation_Two', 'Deed_Of_Variation_Three',
        'Mobility_Grant_Funding_Received', 'Mobility_Grant_Dollar_Size', 
        'Mobility_Grant_Funding_Utilised_2', 'Mobility_Grant_Funding_Remaining_2',
        'Mobility_Grants_Received_2', 'Mobility_Grants_Remaining_2', 'Mobility_Grants_Utilised_2',
        'Internship_Grant_Funding_Received', 'Internship_Grant_Dollar_Size', 'Internship_Grant_Funding_Utilised_2', 'Internship_Grant_Funding_Remaining_2',
        'Internship_Grants_Received_2', 'Internship_Grants_Utilised_2', 'Internship_Grants_Remaining_2',
        'Language_Grant_Funding_Received', 'Language_Grant_Dollar_Size', 'Language_Grant_Funding_Utilised_2', 'Language_Grant_Funding_Remaining_2',
        'Language_Grants_Received_2', 'Language_Grants_Utilised_2', 'Language_Grants_Remaining_2',
        'Administration_Grant_Funding_Received', 'Administration_Grant_Dollar_Size', 'Administration_Grant_Funding_Utilised_2', 'Administration_Grant_Funding_Remaining_2',
        'Administration_Grants_Received_2', 'Administration_Grants_Utilised_2', 'Administration_Grants_Remaining_2',
        'Total_Grant_Funding_Received', 'Total_Grant_Funding_Utilised', 'Total_Grant_Funding_Remaining',
        'Total_Grants_Received', 'Total_Grants_Utilised', 'Total_Grants_Remaining', 'Notes')

    column_labels = {'Program_Name': 'Program Name', 'Program_Acronym': 'Program Acronym', 'Year': 'Year', 'Class_Code': 'Class Code', 
        'Project_Code': 'Project Code', 'ISEO_Code': 'ISEO Code', 'UWA_Mobility_Grant_Project_Grant_Number': 'UWA Mobility Grant Project Grant Number',
        'UWA_Admin_Funding_Project_Grant_Number': 'UWA Admin Funding Project Grant Number', 'Program_Type': 'Program Type', 'Project_Status': 'Project Status',
        'CITIZENS_PR': 'Citizen\'s PR', 'SHORT_TERM_GRANT': 'Short Term Grant', 'SEMESTER_GRANT': 'Semester Grant', 'Funding_Acquittal_Date': 'Funding Acquittal Date', 
        'Project_Completion_Submission_Date': 'Project Completion Submission Date', 'Project_Completion_Report_Link': 'Project Completion Report Link', 
        'Refund_Utilisation_Commonwealth_Date': 'Refund Utilisation Commonwealth Date', 'Commonwealth_Refund_Invoice_Link': 'Commonwealth Refund Invoice Link', 
        'Statutory_Decleration_Date': 'Statutory Decleration Date','Statutory_Decleration_Link': 'Statutory Decleration Link', 'Original_Project_Schedule': 'Original Project Schedule', 
        'Deed_Of_Variation_One': 'Deed Of Variation One', 'Deed_Of_Variation_Two': 'Deed Of Variation Two', 'Deed_Of_Variation_Three': 'Deed Of Variation Three',
        'Mobility_Grant_Funding_Received': 'Mobility Grant Funding Received', 'Mobility_Grant_Dollar_Size': 'Mobility Grant Dollar Size', 'Mobility_Grant_Funding_Utilised_2': 'Mobility Grant Funding Utilised', 
        'Mobility_Grant_Funding_Remaining_2': 'Mobility Grant Funding Remaining', 'Mobility_Grants_Received_2': 'Mobility Grants Received', 'Mobility_Grants_Utilised_2': 'Mobility Grants Utilised', 
        'Mobility_Grants_Remaining_2': 'Mobility Grants Remaining', 'Internship_Grant_Funding_Received': 'Internship Grant Funding Received', 
        'Internship_Grant_Dollar_Size': 'Internship Grant Dollar Size', 'Internship_Grant_Funding_Utilised_2':'Internship Grant Funding Utilised',
        'Internship_Grant_Funding_Remaining_2': 'Internship Grant Funding Remaining', 'Internship_Grants_Received_2': 'Internship Grants Received', 
        'Internship_Grants_Utilised_2': 'Internship Grants Utilised', 'Internship_Grants_Remaining_2': 'Internship Grants Remaining', 
        'Language_Grant_Funding_Received': 'Language Grant Funding Received', 
        'Language_Grant_Dollar_Size': 'Language Grant Dollar Size', 'Language_Grant_Funding_Utilised_2': 'Language Grant Funding Utilised', 'Language_Grant_Funding_Remaining_2': 'Language Grant Funding Remaining',
        'Language_Grants_Received_2': 'Language Grants Received', 'Language_Grants_Utilised_2': 'Language Grants Utilised', 'Language_Grants_Remaining_2': 'Language Grants Remaining',
        'Administration_Grant_Funding_Received': 'Administration Grant Funding Received', 'Administration_Grant_Dollar_Size': 'Administration Grant Dollar Size', 
        'Administration_Grant_Funding_Utilised_2': 'Administration Grant Funding Utilised', 'Administration_Grant_Funding_Remaining_2': 'Administration Grant Funding Remaining',
        'Administration_Grants_Received_2': 'Administration Grants Received', 'Administration_Grants_Utilised_2': 'Administration Grants Utilised', 
        'Administration_Grants_Remaining_2': 'Administration Grants Remaining', 'Total_Grant_Funding_Received': 'Total Grant Funding Received', 'Total_Grant_Funding_Utilised': 'Total Grant Funding Utilised', 
        'Total_Grant_Funding_Remaining': 'Total Grant Funding Remaining', 'Total_Grants_Received': 'Total Grants Received', 'Total_Grants_Utilised': 'Total Grants Utilised', 
        'Total_Grants_Remaining': 'Total Grants Remaining', 'Notes': 'Extra Notes', 'Program_Id': 'Program ID'}

    
    column_descriptions = {'Program_Name': 'Name of Grant Program', 'Program_Acronym': 'Grant Program Acronym', 'Year': 'Year Of Program', 'Class_Code': 'Class Code Of Program',
        'Project_Code': 'Class Code Of Project', 'ISEO_Code': 'ISEO Code Of Program', 'UWA_Mobility_Grant_Project_Grant_Number': 'UWA Mobility Grant Project Grant Number', 
        'UWA_Admin_Funding_Project_Grant_Number': 'UWA_Admin_Funding_Project_Grant_Number', 'Program_Type': 'Type of Program - Short-Term or Semester', 'Project_Status': 'If the Project Funding is Completed', 
        'CITIZENS_PR': 'Not previously Indonesian Citizen and/or Permanent Resident', 'SHORT_TERM_GRANT': 'Previously Received a Short Term Grant', 'SEMESTER_GRANT': 'Previously Received a Semester Grant', 
        'Funding_Acquittal_Date' : '###', 'Project_Completion_Submission_Date': 'Completion Date Of Project', 'Project_Completion_Report_Link': 'Link to Project Completion Report in Dropbox',
        'Refund_Utilisation_Commonwealth_Date': '###', 'Commonwealth_Refund_Invoice_Link': '###', 'Statutory_Decleration_Date': '###', 'Statutory_Decleration_Link': '###', 
        'Original_Project_Schedule': '###', 'Deed_Of_Variation_One': '###', 'Deed_Of_Variation_Two': '###', 'Deed_Of_Variation_Three': '###', 'Mobility_Grant_Funding_Received': 'Value Of Mobility Grant Funding Received',
        'Mobility_Grant_Dollar_Size': 'Mobility Grant Value In Dollars', 'Mobility_Grant_Funding_Utilised_2': 'Value Of Mobility Grant Funding Used', 'Mobility_Grant_Funding_Remaining_2': 'Value Of Mobility Grant Funding Remaining',
        'Mobility_Grants_Received_2': 'Number Of Mobility Grants Received', 'Mobility_Grants_Utilised_2': 'Number Of Mobility Grants Used', 'Mobility_Grants_Remaining_2': 'Number Of Mobility Grants Remaining',
        'Internship_Grant_Funding_Received': 'Value Of Internship Grant Funding Received', 'Internship_Grant_Dollar_Size': 'Internship Grant Value In Dollars', 
        'Internship_Grant_Funding_Utilised_2': 'Value Of Internship Grant Funding Used', 'Internship_Grant_Funding_Remaining_2': 'Value Of Internship Grant Funding Remaining', 
        'Internship_Grants_Received_2': 'Number Of Internship Grants Received', 'Internship_Grants_Utilised_2': 'Number Of Internship Grants Used', 'Internship_Grants_Remaining_2': 'Number Of Internship Grants Remaining',
        'Language_Grant_Funding_Received': 'Value Of Language Grant Funding Received', 'Language_Grant_Dollar_Size': 'Language Grant Value In Dollars', 'Language_Grant_Funding_Utilised_2': 'Value Of Language Grant Funding Used',
        'Language_Grant_Funding_Remaining_2': 'Value Of Language Grant Funding Remaining', 'Language_Grants_Received_2': 'Number Of Language Grants Received', 'Language_Grants_Utilised_2': 'Number Of Language Grants Used',
        'Language_Grants_Remaining_2': 'Number Of Language Grants Remaining', 'Administration_Grant_Funding_Received': 'Value Of Administration Grant Funding Received', 
        'Administration_Grant_Dollar_Size': 'Administration Grant Value In Dollars', 'Administration_Grant_Funding_Utilised_2': 'Value Of Administration Grant Funding Used', 
        'Administration_Grant_Funding_Remaining_2': 'Value Of Administration Grant Funding Remaining', 'Administration_Grants_Received_2': 'Number Of Administration Grants Received',
        'Administration_Grants_Utilised_2': 'Number Of Administration Grants Used', 'Administration_Grants_Remaining_2': 'Number Of Administration Grants Remaining', 
        'Total_Grant_Funding_Received': 'Value Of Total Grant Funding Received', 'Total_Grant_Funding_Utilised': 'Value Of Total Grant Funding Used', 'Total_Grant_Funding_Remaining': 'Value Of Total Grant Funding Remaining',
        'Total_Grants_Received': 'Number Of Total Grants Received', 'Total_Grants_Utilised': 'Number Of Total Grants Used', 'Total_Grants_Remaining': 'Number Of Total Grants Remaining', 
        'Notes': 'Any Extra Notes On The Program', 'Program_Id': 'Program ID'}
    
    # actor_table  = db.select(db.Programs.c.Mobility_Grants_Utilised)
    session = db.Session()
    


    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class UniversitiesModelView(ModelView):
    """Custom view for University. Login secured."""
    list_template = 'list_templates/university_info.html'
    edit_template = 'edit_templates/university_edit.html'
    create_template = 'create_templates/university_create.html'
    details_template = 'details_templates/university_details.html'
    can_export = True 
    export_types = ['csv', 'xls']
    can_edit = True
    can_delete = True
    can_create = True
    can_view_details = True
    can_set_page_size = True
    column_default_sort = 'University_Id' 

    column_searchable_list = ('University_Id', 'University_Acronym', 'University_Name')

    column_list =  ('University_Id', 'University_Acronym', 'University_Name', 'ABN', 'Member_Status_2014', 'Member_Status_2015', 'Member_Status_2016', 'Member_Status_2017',
    'Member_Status_2018', 'Member_Status_2019', 'Member_Status_2020', 'Member_Status_2021', 'Member_Status_2022','Member_Status_2023', 'Member_Status_2024',
    'Member_Status_2025', 'Member_Status_2026', 'Member_Status_2027', 'Member_Status_2028', 'Member_Status_2029', 'Member_Status_2030')

    column_details_list = ('University_Id', 'University_Acronym', 'University_Name', 'ABN', 'Member_Status_2014', 'Member_Status_2015', 'Member_Status_2016', 'Member_Status_2017',
    'Member_Status_2018', 'Member_Status_2019', 'Member_Status_2020', 'Member_Status_2021', 'Member_Status_2022','Member_Status_2023', 'Member_Status_2024',
    'Member_Status_2025', 'Member_Status_2026', 'Member_Status_2027', 'Member_Status_2028', 'Member_Status_2029', 'Member_Status_2030')

    form_columns =  ('University_Id', 'University_Acronym', 'University_Name', 'ABN', 'Member_Status_2014', 'Member_Status_2015', 'Member_Status_2016', 'Member_Status_2017',
    'Member_Status_2018', 'Member_Status_2019', 'Member_Status_2020', 'Member_Status_2021', 'Member_Status_2022','Member_Status_2023', 'Member_Status_2024',
    'Member_Status_2025', 'Member_Status_2026', 'Member_Status_2027', 'Member_Status_2028', 'Member_Status_2029', 'Member_Status_2030')

    column_filters = ('University_Id', 'University_Acronym', 'University_Name', 'ABN', 'Member_Status_2014', 'Member_Status_2015', 'Member_Status_2016', 'Member_Status_2017',
    'Member_Status_2018', 'Member_Status_2019', 'Member_Status_2020', 'Member_Status_2021', 'Member_Status_2022','Member_Status_2023', 'Member_Status_2024',
    'Member_Status_2025', 'Member_Status_2026', 'Member_Status_2027', 'Member_Status_2028', 'Member_Status_2029', 'Member_Status_2030')

    column_sortable_list = ('University_Id', 'University_Acronym', 'University_Name', 'ABN', 'Member_Status_2014', 'Member_Status_2015', 'Member_Status_2016', 'Member_Status_2017',
    'Member_Status_2018', 'Member_Status_2019', 'Member_Status_2020', 'Member_Status_2021', 'Member_Status_2022','Member_Status_2023', 'Member_Status_2024',
    'Member_Status_2025', 'Member_Status_2026', 'Member_Status_2027', 'Member_Status_2028', 'Member_Status_2029', 'Member_Status_2030')

    column_labels = {'ABN': 'ABN', 'University_Acronym': 'University Acronym', 'University_Id': 'University ID', 'University_Name': 'University Name'}

    column_descriptions = {'University_Id': 'Unique University ID', 'University_Acronym': 'Acronym for University' , 'University_Name': 'Name Of Each University', 'ABN': 'ABN Number Of Each University', 
        'Member_Status_2014': 'If The University Was A Member In 2014', 'Member_Status_2015': 'If The University Was A Member In 2015', 'Member_Status_2016': 'If The University Was A Member In 2016', 
        'Member_Status_2017': 'If The University Was A Member In 2017', 'Member_Status_2018': 'If The University Was A Member In 2018', 'Member_Status_2019': 'If The University Was A Member In 2019', 
        'Member_Status_2020': 'If The University Was A Member In 2020', 'Member_Status_2021': 'If The University Was A Member In 2021', 'Member_Status_2022': 'If The University Was A Member In 2022',
        'Member_Status_2023': 'If The University Was A Member In 2023', 'Member_Status_2024': 'If The University Was A Member In 2024', 'Member_Status_2025': 'If The University Was A Member In 2025',
        'Member_Status_2026': 'If The University Was A Member In 2026', 'Member_Status_2027': 'If The University Was A Member In 2027', 'Member_Status_2028': 'If The University Was A Member In 2028', 
        'Member_Status_2029': 'If The University Was A Member In 2029', 'Member_Status_2030': 'If The University Was A Member In 2030'}

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
    column_default_sort = 'Campus_Id'

    column_searchable_list = ('Campus_Id', 'Campus_Name', 'University.University_Name', 'University.University_Acronym', 'University_Id')

    column_list = ('Campus_Id', 'Campus_Name', 'University.University_Name', 'University.University_Acronym', 'Campus_State', 'University_Id')

    column_details_list = ('Campus_Id', 'Campus_Name', 'University.University_Name', 'University.University_Acronym', 'Campus_State', 'University_Id')

    form_columns = ('Campus_Id', 'Campus_Name', 'Campus_State', 'University_Id')

    column_filters = ('Campus_Id', 'Campus_Name', 'University.University_Name', 'University.University_Acronym', 'Campus_State', 'University_Id')
    
    column_sortable_list = ('Campus_Id', 'Campus_Name', 'University.University_Name', 'University.University_Acronym', 'Campus_State', 'University_Id')
       
    column_labels = {'University.University_Acronym': 'University Acronym', 'University.University_Name': 'University Name','Campus_Id': 'Campus ID', 
        'University_Id': 'University ID', 'Campus_Name': 'Campus Name'}

    column_descriptions = {'University.University_Acronym': 'Related University Acronym', 'University.University_Name': 'Related University Name', 
    'Campus_Name': 'Name of Campus', 'Campus_State': 'State Campus is Located', 'Campus_Id': 'Unique Campus ID', 'University_Id': 'Related University ID', }

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
    column_default_sort = 'Payment_Id'

    column_searchable_list = ('Payment_Id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 
        'Payment_Amount', 'Funding_Round', 'Student_Id', 'Program_Id')

    column_list = ('Payment_Id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'UWA_Business_Unit', 
        'Payment_Date', 'Payment_Amount', 'UWA_Account_Number', 'Funding_Round', 'Description', 'Student_Id', 'Program_Id')

    column_details_list = ('Payment_Id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'UWA_Business_Unit', 
        'Payment_Date', 'Payment_Amount', 'UWA_Account_Number', 'Funding_Round', 'Description', 'Student_Id', 'Program_Id')

    form_columns = ('Payment_Id', 'UWA_Business_Unit', 'Payment_Date', 'Payment_Amount', 'UWA_Account_Number', 'Funding_Round', 'Description', 'Student_Id', 'Program_Id')

    column_filters = ('Payment_Id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'UWA_Business_Unit', 
        'Payment_Date', 'Payment_Amount', 'UWA_Account_Number', 'Funding_Round', 'Description', 'Student_Id', 'Program_Id')

    column_sortable_list  = ('Payment_Id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'UWA_Business_Unit', 
        'Payment_Date', 'Payment_Amount', 'UWA_Account_Number', 'Funding_Round', 'Description', 'Student_Id', 'Program_Id')

    column_labels = {'UWA_Business_Unit': 'UWA Business Unit', 'UWA_Account_Number': 'UWA Account Number', 'Payment_Id': 'Payment ID', 
        'Student.First_Name': 'Student First Name', 'Student.Last_Name': 'Student Last Name', 
        'Program.Program_Name': 'Program Name', 'Program.Year': 'Program Year', 'Payment_Amount': 'Payment Amount',
        'Funding_Round': 'Funding Round', 'Student_Id': 'Student ID', 'Program_Id': 'Program ID'}

    column_descriptions = {'Payment_Id': 'Unique Payment ID', 'Student.First_Name': 'Related Student\'s First Name', 'Student.Last_Name': 'Related Student\'s Last Name', 
        'Program.Program_Name': 'Related Program\'s Name', 'Program.Year': 'Related Program\'s Year', 'UWA_Business_Unit': 'UWA\'s Business Unit', 
        'Payment_Date': 'Date of Payment to Student', 'Payment_Amount': 'Amount Paid to Student', 'UWA_Account_Number': 'UWA\'s Account Number for Transaction', 
        'Funding_Round': 'Funding Round Payment is from', 'Description': 'Summary Description of Payment Details', 'Student_Id': 'Related Student ID', 'Program_Id': 'Related Program ID'} 

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
    column_default_sort = 'Grant_Id' 

    column_searchable_list = ('Grant_Id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'Payment.Payment_Amount', 'University.University_Name', 
        'Campus.Campus_Name', 'Period', 'Student_Id', 'Program_Id', 'Payment_Id', 'University_Id', 'Campus_Id', 'Grant_Type')
    
    column_list = ('Grant_Id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'Payment.Payment_Amount', 'University.University_Name', 
        'Campus.Campus_Name', 'Start_Date', 'End_Date', 'Period', 'Grant_Type', 'Awarded', 'Forms_Received', 'Student_Id', 'Program_Id', 'Payment_Id', 'University_Id', 'Campus_Id')
    
    column_details_list = ('Grant_Id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'Payment.Payment_Amount', 'University.University_Name', 
        'Campus.Campus_Name', 'Start_Date', 'End_Date', 'Period', 'Grant_Type', 'Awarded', 'Forms_Received', 'Student_Id', 'Program_Id', 'Payment_Id', 'University_Id', 'Campus_Id')
    
    form_columns = ('Grant_Id', 'Start_Date', 'End_Date', 'Period', 'Grant_Type', 'Awarded', 'Forms_Received', 'Student_Id', 'Program_Id', 'Payment_Id', 'University_Id', 'Campus_Id')
    
    column_filters = ('Grant_Id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'Payment.Payment_Amount', 'University.University_Name', 
        'Campus.Campus_Name', 'Start_Date', 'End_Date', 'Period', 'Grant_Type', 'Awarded', 'Forms_Received', 'Student_Id', 'Program_Id', 'Payment_Id', 'University_Id', 'Campus_Id')
    
    column_sortable_list = ('Grant_Id', 'Student.First_Name', 'Student.Last_Name', 'Program.Program_Name', 'Program.Year', 'Payment.Payment_Amount', 'University.University_Name', 
        'Campus.Campus_Name', 'Start_Date', 'End_Date', 'Period', 'Grant_Type', 'Awarded', 'Forms_Received', 'Student_Id', 'Program_Id', 'Payment_Id', 'University_Id', 'Campus_Id')
    
    column_labels = {'Grant_Id': 'Grant ID', 'Student.First_Name': 'Student First Name', 'Student.Last_Name': 'Student Last Name', 'Program.Program_Name': 'Program Name', 
        'Program.Year': 'Program Year', 'Payment.Payment_Amount': 'Payment Amount', 'University.University_Name': 'University Name', 
        'Campus.Campus_Name': 'Campus Name', 'Start_Date': 'Start Date', 'End_Date': 'End Date', 'Period': 'Period', 'Awarded': 'Awarded',
        'Forms_Received': 'Forms Received', 'Student_Id': 'Student ID', 'Program_Id': 'Program ID', 'Payment_Id': 'Payment ID', 
        'University_Id': 'University ID', 'Campus_Id': 'Campus ID', 'Grant_Type':'Grant Type'}

    column_descriptions = {'Grant_Id': 'Unique Grant ID', 'Student.First_Name': 'Related Student\'s First Name', 'Student.Last_Name': 'Related Student\'s Last Name', 'Program.Program_Name': 'Related Program\'s Name', 
        'Program.Year': 'Related Program\'s Year', 'Payment.Payment_Amount': 'Related Payment Amount', 'University.University_Name': 'Related University\'s Name', 
        'Campus.Campus_Name': 'Related Campus\' Name', 'Start_Date': 'Study Start Date', 'End_Date': 'Study End Date', 'Period': 'Study Period', 'Awarded': 'Program Awarded to Student',
        'Forms_Received': 'Forms Received for Grant to be Processed', 'Student_Id': 'Related Student ID', 'Program_Id': 'Related Program ID', 'Payment_Id': 'Related Payment ID', 
        'University_Id': 'Related University ID', 'Campus_Id': 'Related Campus ID','Grant_Type': "Type of Grant"}

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

class Universities(db.Model):  
    __tablename__ = 'UNIVERSITIES' 
    University_Id = db.Column(db.String(50), primary_key = True) 
    University_Acronym = db.Column(db.String(120))
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

    University = db.relationship(Universities, backref=db.backref('CAMPUSES', uselist=True, lazy='select'))

    def __repr__(self):
        return '<Campus: {}>'.format(self.Campus_Name)


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

    CITIZENS_PR = db.Column(db.Boolean)
    SHORT_TERM_GRANT = db.Column(db.Boolean)
    SEMESTER_GRANT = db.Column(db.Boolean)


    Notes = db.Column(db.String(100))

    University = db.relationship(Universities, backref=db.backref('STUDENTS', uselist=True, lazy='select'))
    Campus = db.relationship(Campuses, backref=db.backref('STUDENTS', uselist=True, lazy='select'))
    
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
    #Eligibility_Ids = db.Column(db.String(50))
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


    Mobility_Grant_Funding_Received = db.Column(db.Integer)
    Mobility_Grant_Dollar_Size = db.Column(db.Integer)

    @hybrid_property
    def Mobility_Grants_Utilised_2(self):
        return object_session(self).query(Grants).filter((Grants.Program_Id == self.Program_Id) & (Grants.Grant_Type == "Mobility")).count()
    @Mobility_Grants_Utilised_2.expression
    def Mobility_Grants_Utilised_2(cls):
        return select([func.count(Grants.Grant_Id)]).where(Grants.Program_Id == cls.Program_Id & (Grants.Grant_Type == "Mobility")).scalar_subquery()

    @hybrid_property
    def Mobility_Grant_Funding_Utilised_2(self):
        return self.Mobility_Grants_Utilised_2 * self.Mobility_Grant_Dollar_Size
    @hybrid_property
    def Mobility_Grant_Funding_Remaining_2(self):
        return self.Mobility_Grant_Funding_Received - self.Mobility_Grant_Funding_Utilised_2
    @hybrid_property
    def Mobility_Grants_Received_2(self):
        try:
            result = self.Mobility_Grant_Funding_Received / self.Mobility_Grant_Dollar_Size
        except ZeroDivisionError:
            result  = 0
        return result
    @hybrid_property
    def Mobility_Grants_Remaining_2(self):
        return self.Mobility_Grants_Received_2 - self.Mobility_Grants_Utilised_2


    Internship_Grant_Funding_Received = db.Column(db.Integer)
    Internship_Grant_Dollar_Size = db.Column(db.Integer)

    @hybrid_property
    def Internship_Grants_Utilised_2(self):
        return object_session(self).query(Grants).filter((Grants.Program_Id == self.Program_Id) & (Grants.Grant_Type == "Internship")).count()
    @Internship_Grants_Utilised_2.expression
    def Internship_Grants_Utilised_2(cls):
        return select([func.count(Grants.Grant_Id)]).where(Grants.Program_Id == cls.Program_Id & (Grants.Grant_Type == "Internship")).scalar_subquery()

    @hybrid_property
    def Internship_Grant_Funding_Utilised_2(self):
        return self.Internship_Grants_Utilised_2 * self.Internship_Grant_Dollar_Size
    @hybrid_property
    def Internship_Grant_Funding_Remaining_2(self):
        return self.Internship_Grant_Funding_Received - self.Internship_Grant_Funding_Utilised_2
    @hybrid_property
    def Internship_Grants_Received_2(self):
        try:
            result = self.Internship_Grant_Funding_Received / self.Internship_Grant_Dollar_Size
        except ZeroDivisionError:
            result  = 0
        return result

    @hybrid_property
    def Internship_Grants_Remaining_2(self):
        print()
        return self.Internship_Grants_Received_2 - self.Internship_Grants_Utilised_2


    Language_Grant_Funding_Received = db.Column(db.Integer)
    Language_Grant_Dollar_Size = db.Column(db.Integer)
   
    @hybrid_property
    def Language_Grants_Utilised_2(self):
        return object_session(self).query(Grants).filter((Grants.Program_Id == self.Program_Id) & (Grants.Grant_Type == "Language")).count()
    @Language_Grants_Utilised_2.expression
    def Language_Grants_Utilised_2(cls):
        return select([func.count(Grants.Grant_Id)]).where(Grants.Program_Id == cls.Program_Id & (Grants.Grant_Type == "Language")).scalar_subquery()
   
    @hybrid_property
    def Language_Grant_Funding_Utilised_2(self):
        return self.Language_Grants_Utilised_2 * self.Language_Grant_Dollar_Size
    @hybrid_property
    def Language_Grant_Funding_Remaining_2(self):
        return self.Language_Grant_Funding_Received - self.Language_Grant_Funding_Utilised_2
    @hybrid_property
    def Language_Grants_Received_2(self):
        try:
            result = self.Language_Grant_Funding_Received / self.Language_Grant_Dollar_Size
        except ZeroDivisionError:
            result  = 0
        return result
    @hybrid_property
    def Language_Grants_Remaining_2(self):
        return self.Language_Grants_Received_2 - self.Language_Grants_Utilised_2


    Administration_Grant_Funding_Received = db.Column(db.Integer)
    Administration_Grant_Dollar_Size = db.Column(db.Integer)

    @hybrid_property
    def Administration_Grants_Utilised_2(self):
        return object_session(self).query(Grants).filter((Grants.Program_Id == self.Program_Id) & (Grants.Grant_Type == "Administration")).count()
    @Administration_Grants_Utilised_2.expression
    def Administration_Grants_Utilised_2(cls):
        return select([func.count(Grants.Grant_Id)]).where(Grants.Program_Id == cls.Program_Id & (Grants.Grant_Type == "Administration")).scalar_subquery()

    @hybrid_property
    def Administration_Grant_Funding_Utilised_2(self):
        return self.Administration_Grants_Utilised_2 * self.Administration_Grant_Dollar_Size
    @hybrid_property
    def Administration_Grant_Funding_Remaining_2(self):
        return self.Administration_Grant_Funding_Received - self.Administration_Grant_Funding_Utilised_2
    @hybrid_property
    def Administration_Grants_Received_2(self):
        try:
            result = self.Administration_Grant_Funding_Received / self.Administration_Grant_Dollar_Size
        except ZeroDivisionError:
            result  = 0
        return result
    @hybrid_property
    def Administration_Grants_Remaining_2(self):
        return self.Administration_Grants_Received_2 - self.Administration_Grants_Utilised_2

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

    Program = db.relationship(Programs, backref=db.backref('PAYMENTS', uselist=True, lazy='select'))
    Student = db.relationship(Students, backref=db.backref('PAYMENTS', uselist=True, lazy='select'))

    def __repr__(self):
        return '<Payments: {}>'.format(self.Payment_Id, self.Student_Id, self.Payment_Amount)


class Grants(db.Model):  
    __tablename__ = 'GRANTS' 
    Grant_Id = db.Column(db.String(50), primary_key = True) 
    Start_Date = db.Column(db.Date)
    End_Date = db.Column(db.Date)
    Period = db.Column(db.String(50))
    Program_Id = db.Column(db.String(50), db.ForeignKey("PROGRAMS.Program_Id"))
    Student_Id = db.Column(db.String(50), db.ForeignKey("STUDENTS.Student_Id"))
    Payment_Id = db.Column(db.String(50), db.ForeignKey("PAYMENTS.Payment_Id"))
    University_Id = db.Column(db.String(50), db.ForeignKey("UNIVERSITIES.University_Id"))
    Campus_Id = db.Column(db.String(50), db.ForeignKey("CAMPUSES.Campus_Id"))
    Grant_Type = db.Column(db.String(50))
    Awarded = db.Column(db.Boolean)
    Forms_Received = db.Column(db.Boolean)    
    University = db.relationship(Universities, backref=db.backref('GRANTS', uselist=True, lazy='select'))
    Program = db.relationship(Programs, backref=db.backref('GRANTS', uselist=True, lazy='select'))
    Student = db.relationship(Students, backref=db.backref('GRANTS', uselist=True, lazy='select'))
    Campus = db.relationship(Campuses, backref=db.backref('GRANTS', uselist=True, lazy='select'))
    Payment = db.relationship(Payments, backref=db.backref('GRANTS', uselist=True, lazy='select'))
    
    def __repr__(self):
        return '<Grant {} {} {}>'.format(self.Grant_Id, self.Program_Id, self.Student_Id)  


# #Functions to import csv files from github
# def pd_access():
#     # Username of your GitHub account
#     username = '' 

#     # Personal Access Token (PAO) from your GitHub account
#     token = ''

#     # Creates a re-usable session object with your creds in-built
#     github_session = requests.Session()
#     github_session.auth = (username, token)
#     return github_session

#function to download files two ways
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
        data = Campuses(Campus_Id = row['CAMPUS_ID (PK)'],  University_Id = row['UNIVERSITY_ID (FK)'] ,Campus_Name = row['CAMPUS_NAME'] ,Campus_State = row['CAMPUS_STATE'])
        db.session.add(data)
        db.session.commit()

def load_pd_df_Grants(df):
    for index, row in df.iterrows():
        data= Grants(Grant_Id=row["GRANT_ID (PK)"],Start_Date=datetime.strptime(row["START_DATE"],'%d/%m/%Y').date(),End_Date=datetime.strptime(row["END_DATE"],'%d/%m/%Y').date(), Period = row['PERIOD'], Program_Id=row["PROGRAM_ID (FK)"], Student_Id=row["STUDENT_ID (FK)"], Payment_Id=row["PAYMENT_ID (FK)"], University_Id=row["UNIVERSITY_ID (FK)"], Campus_Id=row["CAMPUS_ID (FK)"], Grant_Type =row["GRANT_TYPE"], Awarded=str2bool(row["AWARDED"]), Forms_Received=str2bool(row["FORMS_RECEIVED"]))
        db.session.add(data)
        db.session.commit()  

def load_pd_df_Universities(df):
    for index, row in df.iterrows():
        data = Universities(University_Id =row['UNIVERSITY_ID (PK)'], University_Acronym = row['UNIVERSITY_ACRONYM'],University_Name = row['UNIVERSITY_NAME'], ABN=  row['ABN'], Member_Status_2014= str2bool(row["MEMBER_STATUS_2014"]), Member_Status_2015= str2bool(row["MEMBER_STATUS_2015"]), Member_Status_2016= str2bool(row["MEMBER_STATUS_2016"]), Member_Status_2017=str2bool(row["MEMBER_STATUS_2017"]),
        Member_Status_2018=str2bool(row["MEMBER_STATUS_2018"]), Member_Status_2019=str2bool(row["MEMBER_STATUS_2019"]), Member_Status_2020=str2bool(row["MEMBER_STATUS_2020"]), Member_Status_2021=str2bool(row["MEMBER_STATUS_2021"]), Member_Status_2022=str2bool(row["MEMBER_STATUS_2022"]),
        Member_Status_2023=str2bool(row["MEMBER_STATUS_2023"]), Member_Status_2024=str2bool(row["MEMBER_STATUS_2024"]), Member_Status_2025=str2bool(row["MEMBER_STATUS_2025"]), Member_Status_2026=str2bool(row["MEMBER_STATUS_2026"]), Member_Status_2027=str2bool(row["MEMBER_STATUS_2027"]),
        Member_Status_2028=str2bool(row["MEMBER_STATUS_2028"]), Member_Status_2029=str2bool(row["MEMBER_STATUS_2029"]), Member_Status_2030=str2bool(row["MEMBER_STATUS_2030"]))
        db.session.add(data)
        db.session.commit()    

def load_pd_df_Payments(df):
    for index, row in df.iterrows():
        data= Payments(Payment_Id=row["PAYMENT_ID"], Student_Id=row["STUDENT_ID (FK)"], Program_Id=row["PROGRAM_ID (FK)"], UWA_Business_Unit=row["UWA_BUSINESS_UNIT"], Payment_Date=datetime.strptime(row["PAYMENT_DATE"],'%d/%m/%Y').date(), Payment_Amount=row["PAYMENT_AMOUNT"],
        UWA_Account_Number=row["UWA_ACCOUNT_NUMBER"], Funding_Round=row["FUNDING_ROUND"], Description=row["DESCRIPTION"])
        db.session.add(data)
        db.session.commit()  

def load_pd_df_Programs(df):
    names = list(df.keys())
    for index, row in df.iterrows():
        data = Programs(Program_Id=row["PROGRAM_ID (PK)"], Program_Name=row["PROGRAM_NAME"], Program_Acronym=row["PROGRAM_ACRONYM"], Year=row["YEAR"], Class_Code=row["CLASS_CODE"], Project_Code=row["PROJECT_CODE"], ISEO_Code=row["ISEO_CODE"], UWA_Mobility_Grant_Project_Grant_Number=row["UWA_MOBILITY_GRANT_PROJECT_GRANT_NUMBER"],
        UWA_Admin_Funding_Project_Grant_Number=row["UWA_ADMIN_FUNDING_PROJECT_GRANT_NUMBER"], Program_Type=row["PROGRAM_TYPE"], Project_Status=row["PROJECT_STATUS"], CITIZENS_PR=str2bool(row["CITIZENS_PR"]), SHORT_TERM_GRANT=str2bool(row["SHORT_TERM_GRANT"]), SEMESTER_GRANT=str2bool(row["SEMESTER_GRANT"]),Funding_Acquittal_Date=datetime.strptime(row["FUNDING_ACQUITTAL _DATE"],'%d/%m/%Y').date(), Project_Completion_Submission_Date=datetime.strptime(row["PROJECT_COMPLETION_SUBMISSION_DATE"],'%d/%m/%Y').date(),
        Project_Completion_Report_Link=row["PROJECT_COMPLETION_REPORT_LINK"], Refund_Utilisation_Commonwealth_Date=datetime.strptime(row["REFUND_UTILISATION_COMMONWEALTH_DATE"],'%d/%m/%Y').date(), Commonwealth_Refund_Invoice_Link=row["COMMONWEALTH_REFUND_INVOICE_LINK"], Statutory_Decleration_Date=datetime.strptime(row["STATUTORY_DECLORATION_DATE"],'%d/%m/%Y').date(),
        Statutory_Decleration_Link=row["STATUTORY_DECLARATION_LINK"], Original_Project_Schedule=row["ORIGINAL_PROJECT_SCHEDULE_LINK"], Deed_Of_Variation_One=row["DEED_OF_VARIATION_1_LINK"], Deed_Of_Variation_Two=row["DEED_OF_VARIATION_2_LINK"], Deed_Of_Variation_Three=row["DEED_OF_VARIATION_3_LINK"],
        Mobility_Grant_Funding_Received=row["MOBILITY_GRANT_FUNDING_RECIEVED"], Mobility_Grant_Dollar_Size=row["MOBILITY_GRANT_DOLLAR_SIZE"],
        Internship_Grant_Funding_Received=row["INTERNSHIP_GRANT_FUNDING_RECIEVED"], Internship_Grant_Dollar_Size=row["INTERNSHIP_GRANT_DOLLAR_SIZE"],
        Language_Grant_Funding_Received=row["LANGUAGE_GRANT_FUNDING_RECIEVED"], Language_Grant_Dollar_Size=row["LANGUAGE_GRANT_DOLLAR_SIZE"],
        Administration_Grant_Funding_Received=row["ADMINISTRATION_GRANT_FUNDING_RECIEVED"], Administration_Grant_Dollar_Size=row["ADMINISTRATION_GRANT_DOLLAR_SIZE"],
        Total_Grant_Funding_Received=row["TOTAL_GRANT_FUNDING_RECIEVED"], Total_Grant_Funding_Utilised=row["TOTAL_GRANT_FUNDING_UTILISED"], Total_Grant_Funding_Remaining=row["TOTAL_GRANT_FUNDING_REMAINING"],
        Total_Grants_Received=row["TOTAL_GRANTS_RECEIVED"], Total_Grants_Utilised=row["TOTAL_GRANTS_UTILISED"], Total_Grants_Remaining=row["TOTAL_GRANTS_REMAINING"], Notes = row["NOTES"])
        db.session.add(data)
        db.session.commit()

def load_pd_df_Students(df):
    for index, row in df.iterrows():
        data = Students(Student_Id=row["STUDENT_ID (PK)"],University_Id = row["UNIVERSITY_ID (FK)"], Campus_Id = row["CAMPUS_ID (FK)"],Student_Number = row["STUDENT_NUMBER"],Title=row["TITLE"], First_Name=row["FIRST_NAME"], 
        Preferred_Name=row["PREFERRED_NAME"], Last_Name=row["LAST_NAME"], Address_Line_One=row["ADDRESS_LINE_1"], Address_Line_Two=row["ADDRESS_LINE_2"], City=row["CITY"], Postcode=row["POSTCODE"], State=row["STATE"], Country=row["COUNTRY"], Date_Of_Birth=datetime.strptime(row["DATE_OF_BIRTH"],'%d/%m/%Y').date(), Phone_Number=row["PHONE_NUMBER"], 
        Student_Email=row["STUDENT_EMAIL"], Gender=row["GENDER"], BSB=row["BSB"], Account_Number=row["ACCOUNT_NUMBER"], Field_Of_Study=row["FIELD_OF_STUDY_CODE"], Country_Of_Birth=row["COUNTRY_OF_BIRTH"],Indigenous_Australian= str2bool(row["INDIGENOUS_AUSTRALIAN"]), Disability= str2bool(row["DISABILITY"]), Aus_Citizen= str2bool(row["AUS_CITIZEN"]), CITIZENS_PR=str2bool(row["CITIZENS_PR"]), SHORT_TERM_GRANT=str2bool(row["SHORT_TERM_GRANT"]), SEMESTER_GRANT=str2bool(row["SEMESTER_GRANT"]), Notes=row["NOTES"])
        db.session.add(data)
        db.session.commit()


#Dummy data uploaded. Uncoment if you need tp populate the database again. 
# #github_session = pd_access()
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

