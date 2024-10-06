import unittest
import json
import time
from app import app, db, Organization, Employee

class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a test client
        cls.app = app.test_client()
        cls.app_context = app.app_context()
        cls.app_context.push()

        # Create the database and the tables
        db.create_all()

        # Add test data
        organization = Organization(name="Test Org", display_columns=["first_name", "last_name"])
        db.session.add(organization)
        db.session.commit()

        employee = Employee(first_name="John", last_name="Doe", email="john@example.com",
                            department="HR", location="Office", position="Manager",
                            organization_id=organization.id)
        db.session.add(employee)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        # Drop all tables after tests
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_search_employees_success(self):
        response = self.app.get('/employees/search?org_id=1&query=John&page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn("results", data)
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["first_name"], "John")
        self.assertEqual(data["results"][0]["last_name"], "Doe")

    def test_search_employees_org_not_found(self):
        response = self.app.get('/employees/search?org_id=999&query=John&page=1&per_page=10')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Organization not found.")

    def test_search_employees_missing_org_id(self):
        response = self.app.get('/employees/search?query=John&page=1&per_page=10')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Organization ID is required.")

if __name__ == '__main__':
    unittest.main()
