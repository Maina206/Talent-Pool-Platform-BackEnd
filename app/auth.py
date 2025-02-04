from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Employee, Employer, Jobs
from datetime import timedelta
import re


auth_bp = Blueprint('auth', __name__)

# Helper functions
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_password(password):
    return len(password) >= 6

# Registration Routes
@auth_bp.route('/register/developer', methods=['POST'])
def register_developer():
    try:
        data = request.get_json()
        
        # Check that all required fields are provided
        if not all(k in data for k in ['email', 'password', 'first_name', 'last_name']):
            return jsonify({"error": "Missing required fields"}), 400
        
        email = data['email'].strip()
        password = data['password'].strip()

        # Validate email and password
        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400
        if not is_valid_password(password):
            return jsonify({"error": "Password must be at least 6 characters"}), 400

        # Check if email already exists
        if Employee.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 400

        
        # Create a new employee record
        new_employee = Employee(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data.get('role'),
            phone=data.get('phone'),
            experience=data.get('experience'),
            programming_languages=",".join(data.get('languages', [])),
            bio=data.get('bio'),
            education=data.get('education'),
            availability=data.get('availability'),
        )
        
        # Hash the password
        new_employee.set_password(data['password'])

        # Add new employee to the database
        db.session.add(new_employee)
        db.session.commit()

        return jsonify(new_employee.to_json()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/register/employer', methods=['POST'])
def register_employer():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        

        # Check that all required fields are provided
        if not all(k in data for k in ['email', 'password', 'first_name', 'last_name', 'company_name']):
            return jsonify({"error": "Missing required fields"}), 400
        

        # Validate email and password
        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400
        if not is_valid_password(password):
            return jsonify({"error": "Password must be at least 6 characters"}), 400

        # Check if email already exists
        if Employer.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 400

        # Hash the password
        hashed_password = generate_password_hash(password)
        
        # Create a new employer record
        new_employer = Employer(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            company_name=data['company_name'],
            phone=data.get('phone', '')
        )
        
        new_employer.set_password(data['password'])

        # Add new employer to the database
        db.session.add(new_employer)
        db.session.commit()

        return jsonify({
            "message": "Registration successful",
            "user": {
                "id": new_employer.id,
                "email": new_employer.email,
                "first_name": new_employer.first_name,
                "last_name": new_employer.last_name,
                "company_name": new_employer.company_name,
                "user_type": "employer"
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    
 # Employer Login Route
@auth_bp.route('/login/employer', methods=['POST'])
def employer_login():
    # Validate request content type
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    data = request.get_json()

    # Validate required fields
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing email or password"}), 400

    email = data.get('email')
    password = data.get('password')

    # Fetch the employer from the database
    employer = Employer.query.filter_by(email=email).first()

    # If the employer is not found, return 401 (Unauthorized) instead of 404
    if not employer:
        return jsonify({"message": "Invalid credentials"}), 401
    
    # Check password
    if not employer.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401
    
    # Create access token
    access_token = create_access_token(identity=employer.get_id(), expires_delta=timedelta(days=3))

    # Return successful login response
    return jsonify({
        'message': 'Employer Login successful!',
        'access_token': access_token,
        'user': employer.to_json(),
    }), 200

# Employee Login Route
@auth_bp.route('/login/developer', methods=['POST'])
def employee_login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    # Fetch the employee from the database
    employee = Employee.query.filter_by(email=email).first()

    # If the employee is not found or password does not match, return error
    if not employee:
        return jsonify({"message": "Employee not found"}), 404
    
    if not employee.check_password(password):  # Ensure check_password is called correctly
        return jsonify({"message": "Invalid credentials"}), 401
    
    # Set the expiration time to 3 days
    access_token = create_access_token(identity=employee.get_id(), expires_delta=timedelta(days=3))

    # Return the successful login response with the access token
    return jsonify({
        'message': 'Employee Login successful!',
        'access_token': access_token,
        'user': employee.to_json(),
    }), 200   



# Protected route example
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = Employee.query.get(current_user_id) or Employer.query.get(current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_type": "developer" if isinstance(user, Employee) else "employer"
    }

    if isinstance(user, Employer):
        user_data["company_name"] = user.company_name
    elif isinstance(user, Employee):
        user_data.update({
            "role": user.role,
            "experience": user.experience,
            "programming_languages": user.programming_languages,
            "bio": user.bio,
            "education": user.education,
            "availability": user.availability
        })

    return jsonify(user_data), 200


