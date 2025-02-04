from werkzeug.security import generate_password_hash, check_password_hash
from . import db  
from flask_login import UserMixin

class Employer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Hashed password
    
    def __repr__(self):
        return f'<Employer {self.first_name} {self.last_name}>'

    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name":self.last_name,
            "password":self.password,
            "email": self.email,
        }

    # Hash the password before saving it
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Check if the entered password matches the hashed password
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    programming_languages = db.Column(db.Text, nullable=False)  # Store as a comma-separated string
    bio = db.Column(db.Text, nullable=False)
    education = db.Column(db.Text, nullable=False)
    availability = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False) 
    
    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'

    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name":self.last_name,
            "password":self.password,
            "email": self.email,
        }

    # Hash the password before saving it
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Check if the entered password matches the hashed password
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)
    

class Jobs(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    experience_required = db.Column(db.Integer, nullable=False)
    job_type = db.Column(db.String(50), nullable=True)
    application_deadline = db.Column(db.Date, nullable=True)
    job_status = db.Column(db.String(50), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    
    # employer = db.relationship('Employer', back_populates='jobs')
    # employee = db.relationship('Employee', back_populates='jobs')