import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

'''from models.py import Base, Panel


class TestQuery(unittest.TestCase):

    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    session = Session()

    def setUp(self):
        Base.metadata.create_all(self.engine)
        self.session.add(Panel(1, 'ion torrent', 'start'))
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_query_panel(self):
        expected = [Panel(1, 'ion torrent', 'start')]
        result = self.session.query(Panel).all()
        self.assertEqual(result, expected) '''