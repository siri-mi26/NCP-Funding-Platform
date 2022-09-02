from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
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

class Student(db.Model):  
    __tablename__ = 'Student' 
    id = db.Column(db.Integer, primary_key = True) 
    student_Number = db.Column(db.Integer)
    First_Name = db.Column(db.String(50))
    Last_Name = db.Column(db.String(50))
    University = db.Column(db.String(50)) #could be foreign key to diff table
    
    def __repr__(self):
        return '<Student {}>'.format(self.studentnumber)

class University(db.Model):  
    __tablename__ = 'University' 
    id = db.Column(db.Integer, primary_key = True) 
    Name = db.Column(db.Integer)
    Member_Status = db.Column(db.String(50))

    def __repr__(self):
        return '<University {}>'.format(self.Name)

class Grants(db.Model):  
    __tablename__ = 'Grants' 
    id = db.Column(db.Integer, primary_key = True) 
    Name = db.Column(db.Integer)

    def __repr__(self):
        return '<Grant {}>'.format(self.Name)
        
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
