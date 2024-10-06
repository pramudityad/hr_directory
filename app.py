from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import asyncio

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hr_directory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Flask-Limiter
limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Apply the limiter to the app
limiter.init_app(app)

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    display_columns = db.Column(db.PickleType, default=list)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

    __table_args__ = (
        Index('idx_first_last_name', 'first_name', 'last_name'),
    )

# Create the database tables within an application context
def create_db():
    with app.app_context():
        db.create_all()

@app.route('/employees/search', methods=['GET'])
@limiter.limit("10 per minute")  # Rate limit for this specific endpoint
async def search_employees():
    org_id = request.args.get('org_id')
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if not org_id:
        return jsonify({"error": "Organization ID is required."}), 400

    organization = Organization.query.get(org_id)
    if not organization:
        return jsonify({"error": "Organization not found."}), 404

    # Using ilike for case-insensitive search
    search_filter = (
        Employee.first_name.ilike(f'%{query}%') |
        Employee.last_name.ilike(f'%{query}%')
    )

    # Paginate the results
    employees_query = Employee.query.filter(
        Employee.organization_id == org_id,
        search_filter
    )

    paginated_employees = employees_query.paginate(page=page, per_page=per_page, error_out=False)

    display_columns = organization.display_columns
    result = []

    for emp in paginated_employees.items:
        emp_data = {col: getattr(emp, col) for col in display_columns if hasattr(emp, col)}
        result.append(emp_data)

    return jsonify({
        'page': paginated_employees.page,
        'total_pages': paginated_employees.pages,
        'total_results': paginated_employees.total,
        'results': result
    })


# Call the create_db function to set up the database
if __name__ == '__main__':
    create_db()
    app.run(debug=True)
