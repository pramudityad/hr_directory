from app import app, db, Organization, Employee

def populate_db():
    with app.app_context():  # Create an application context
        # Create the database tables
        db.create_all()

        org1 = Organization(name='Tech Corp', display_columns=['first_name', 'last_name', 'email', 'department'])
        db.session.add(org1)
        db.session.commit()

        # Add sample employees
        emp1 = Employee(first_name='John', last_name='Doe', email='john.doe@example.com', 
                        department='Engineering', location='New York', position='Software Engineer', 
                        organization_id=org1.id)
        emp2 = Employee(first_name='Jane', last_name='Smith', email='jane.smith@example.com', 
                        department='HR', location='Los Angeles', position='HR Manager', 
                        organization_id=org1.id)

        db.session.add(emp1)
        db.session.add(emp2)
        db.session.commit()

if __name__ == '__main__':
    populate_db()
