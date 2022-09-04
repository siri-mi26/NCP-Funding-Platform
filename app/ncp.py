from app import app,db
from app.models import Users, Students

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': Users, 'Student': Students}