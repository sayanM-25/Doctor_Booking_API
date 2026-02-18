# Doctor_Booking_API

Doctor_Booking_API is a RESTful backend service built using Django and Django REST Framework that allows patients to browse doctors, book appointments, and manage their bookings. This API provides secure authentication and efficient management of doctor availability and appointment scheduling.

---

## Features

- User Registration and Authentication (Token-based)
- Doctor listing and profile management
- Appointment booking system
- View, update, and cancel appointments
- Doctor availability management
- Secure REST API endpoints
  
---

## Tech Stack

- Backend: Django, Django REST Framework
- Database: SQLite (default)
- Authentication: Token Authentication
- Language: Python 3

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/...
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

#### Windows:
```bash
venv\Scripts\activate
```
#### Mac/Linux:
```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

#### Server will run at:
```cpp
http://127.0.0.1:8000/
```

#### Settings.py:
Change EMAIL_HOST_USER='your email' and EMAIL_HOST_PASSWORD='password'

