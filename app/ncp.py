from app import app,db
from app.models import  Users, Students, Programs, Universities, Campuses, Grants, ProgramsByUniversity, ProgramsByUniversity

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users, 'Students': Students, 'Programs': Programs, "Universities": Universities, "Campuses": Campuses, 'Grants':Grants, 'ProgramsByUniversity': ProgramsByUniversity, 'ProgramsByUniversity': ProgramsByUniversity}