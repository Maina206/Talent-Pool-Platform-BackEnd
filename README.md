# Talent Pool App - Backend

## Overview

Backend API service for the Talent Pool App, handling user authentication, profile management, and data persistence. Currently supports basic user authentication and profile management features.

## Current Features

- User authentication system for employers and developers
- Developer profile management
- Database operations for user data
- RESTful API endpoints

## Technologies Used

- Flask (Python web framework)
- SQLAlchemy ORM
- PostgreSQL database
- Render platform for deployment

## Prerequisites

- Python 3.8 or higher
- PostgreSQL
- pip (Python package manager)

## Installation

1. Clone the repository

```bash
git clone [Your Repository URL]
cd talent-pool-backend
```

2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # For Unix
# or
.\venv\Scripts\activate  # For Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure environment variables
   Create a `.env` file and add:

```
DATABASE_URL=your_postgres_database_url
SECRET_KEY=your_secret_key
```

5. Initialize the database

```bash
flask db upgrade
```

6. Run the development server

```bash
flask run
```

## API Documentation

Base URL: [Your API URL](your-api-url-here)

### Current Endpoints

```
Authentication:
POST /api/auth/signup
POST /api/auth/login

Profiles:
GET /api/profiles
GET /api/profiles/<id>
POST /api/profiles
PATCH /api/profiles/<id>
```

## Database Schema

```sql
Users Table:
- id (Primary Key)
- email
- password_hash
- user_type (developer/employer)
- created_at

Profiles Table:
- id (Primary Key)
- user_id (Foreign Key)
- name
- skills
- experience
- education
- availability_status
```

## Deployment

The application is deployed on Render. To deploy your own instance:

1. Create a new Web Service on Render
2. Connect your repository
3. Configure environment variables
4. Deploy the application

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request

## Contact

Alexander Maina - [Your Contact Information]

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
