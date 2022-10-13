from app import app,db
from app.models import  Users, Students, Programs, Payments, Universities, Campuses, Grants, ProgramsByUniversity, UniversitiesFunding

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users, 'Students': Students, 'Programs': Programs, 'Payments': Payments, "Universities": Universities, "Campuses": Campuses, 'Grants':Grants, 'ProgramsByUniversity': ProgramsByUniversity, 'UniversitiesFunding': UniversitiesFunding}