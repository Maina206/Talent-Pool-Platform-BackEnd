from flask import Flask, Blueprint, request, jsonify, redirect, url_for
from .models import Employer, Employee, Jobs, db
from .email_service import send_email
import datetime

main = Blueprint('main', __name__)

# Employer Routes
# =================================================================
# Employer can view all the employees
@main.route("/employer/<int:id>/view_all_employees", methods=["GET"])
def view_all_employees(id):
    employer = Employer.query.get(id)
    if not employer:
        return jsonify({"message": "Employer not found"}), 404

    employees = Employee.query.all()
    employee_list = [{"id": e.id, "first_name": e.first_name, "last_name": e.last_name, "role": e.role} for e in employees]
    
    return jsonify(employee_list)

# Employer can view employee profile
@main.route("/employer/<int:id>/employee/<int:employee_id>", methods=["GET"])
def view_employee_profile(id, employee_id):
    employer = Employer.query.get(id)
    if not employer:
        return jsonify({"message": "Employer not found"}), 404

    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"message": "Employee not found"}), 404
    
    employee_data = {
        "id": employee.id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "role": employee.role,
        "email": employee.email,
        "phone": employee.phone,
        "experience": employee.experience,
        "programming_languages": employee.programming_languages,
        "bio": employee.bio,
        "education": employee.education,
        "availability": employee.availability,
    }

    return jsonify(employee_data)

# Employer can send email to employees
@main.route("/employer/<int:id>/send_email", methods=["POST"])
def send_email_to_employee(id):
    employer = Employer.query.get(id)
    if not employer:
        return jsonify({"message": "Employer not found"}), 404

    data = request.get_json()
    employee = Employee.query.get(data['employee_id'])
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    send_email(employee.email, data['subject'], data['message'])
    return jsonify({"message": "Email sent successfully"}), 200

# Employer can favorite employees and view them
@main.route("/employer/<int:id>/favorite/<int:employee_id>", methods=["POST"])
def favorite_employee(id, employee_id):
    employer = Employer.query.get(id)
    if not employer:
        return jsonify({"message": "Employer not found"}), 404

    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    employer.favorites.append(employee)
    db.session.commit()

    return jsonify({"message": "Employee added to favorites"}), 200

# Employer can create jobs with the following fields: class Jobs(db.Model, UserMixin):
@main.route("/employer/<int:id>/create_job", methods=["POST"])
def create_job(id):
    employer = Employer.query.get(id)
    if not employer:
        return jsonify({"message": "Employer not found"}), 404

    data = request.get_json()

    new_job = Jobs(
    title=data['title'],
    description=data['description'],
    company_name=employer.company_name,
    location=data['location'],
    salary=data['salary'],
    experience_required=data['experience_required'],
    job_type=data['job_type'],
    application_deadline=data.get('application_deadline', datetime.date.today()),  # Default to today's date
    job_status=data.get('job_status', 'open'),  # Default to 'open' if not provided
    employer_id=employer.id  # Employer id passed as argument
    )


    db.session.add(new_job)
    db.session.commit()

    return jsonify({"message": "Job created successfully", "job_id": new_job.id}), 201



# Employer removing an employee from favorites
@main.route("/employer/<int:id>/remove_favorite/<int:employee_id>", methods=["DELETE"])
def remove_favorite_employee(id, employee_id):
    employer = Employer.query.get(id)
    if not employer:
        return jsonify({"message": "Employer not found"}), 404

    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    employer.favorites.remove(employee)
    db.session.commit()

    return jsonify({"message": "Employee removed from favorites"}), 200


# Employee Routes
# =================================================================
# Employee can edit his profile
@main.route("/employee/<int:id>/edit", methods=["PUT"])
def edit_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    data = request.get_json()

    employee.first_name = data.get('first_name', employee.first_name)
    employee.last_name = data.get('last_name', employee.last_name)
    employee.role = data.get('role', employee.role)
    employee.email = data.get('email', employee.email)
    employee.phone = data.get('phone', employee.phone)
    employee.experience = data.get('experience', employee.experience)
    employee.programming_languages = data.get('programming_languages', employee.programming_languages)
    employee.bio = data.get('bio', employee.bio)
    employee.education = data.get('education', employee.education)
    employee.availability = data.get('availability', employee.availability)

    db.session.commit()

    return jsonify({"message": "Employee profile updated successfully"}), 200

# Employee can view other employees
@main.route("/employee/view_all", methods=["GET"])
def view_all_employees_for_employee():
    employees = Employee.query.all()
    employee_list = [{"id": e.id, "first_name": e.first_name, "last_name": e.last_name, "role": e.role} for e in employees]
    return jsonify(employee_list)

# Employee can send email to Employer
@main.route("/employee/send_email", methods=["POST"])
def send_email_from_employee():
    data = request.get_json()
    employee = Employee.query.get(data['employee_id'])
    employer = Employer.query.get(data['employer_id'])

    if not employee and not employer:
        return jsonify({"message": "Invalid employee or employer"}), 404

    send_email(data['recipient_email'], data['subject'], data['message'])
    return jsonify({"message": "Email sent successfully"}), 200
