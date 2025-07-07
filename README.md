# Accounting Software - Django-Based Solution

## Overview

This is a comprehensive accounting software built with Django and Django Templates that provides essential financial management features for small to medium-sized businesses. The application includes modules for sales, purchases, expenses, customer management, and inventory tracking.

## Features

### Core Modules
- **Sales Management**
  - Create and manage sales invoices
  - Track customer orders
  - Generate sales reports
- **Purchase Management**
  - Record vendor purchases
  - Manage purchase orders
  - Track inventory procurement
- **Expense Tracking**
  - Categorize and record business expenses
  - Generate expense reports
  - Monitor cash flow
- **Customer Management**
  - Maintain customer database
  - Track customer transactions
  - Manage customer accounts
- **Inventory Management**
  - Track stock levels
  - Manage product catalog
  - Set low stock alerts
  - Record inventory movements

### Additional Features
- User authentication and authorization
- Dashboard with key financial metrics
- Financial reporting (profit/loss, balance sheet)
- Tax calculation and management
- Multi-user support with role-based permissions

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: Django Templates, HTML, CSS, JavaScript
- **Database**: SQLite (default, can be configured for PostgreSQL/MySQL)
- **Dependencies**: See requirements.txt

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtualenv (recommended)

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd accounting-software
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure database settings in `settings.py` if needed (default uses SQLite)

5. Apply migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application at `http://localhost:8000`

## Usage

1. Log in with your superuser credentials
4. Add products/services to your inventory
5. Begin recording transactions
