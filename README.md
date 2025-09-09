# Finance Django API

This project is a Django-based backend for a personal finance management system.

## Features

- JWT Authentication with access & refresh tokens stored in cookies
- User registration and login
- Income and Expense management
- Dashboard summary API
- RESTful API endpoints for CRUD operations
- CORS ready for frontend integration

## Installation

1. Clone the repository:
```bash
git clone <your-repo-link>

Install dependencies:
pip install -r requirements.txt

Configure your .env file for database and secret keys.

Apply migrations:
python manage.py migrate

Run the server:
python manage.py runserver

API Endpoints

POST /api/register/ - Register a new user

POST /api/login/ - Login and get JWT cookies

GET /api/logout/ - Logout and delete cookies

GET /api/dashboard/ - Get summary of incomes and expenses

CRUD /api/incomes/ - Manage incomes

CRUD /api/expenses/ - Manage expenses

*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-