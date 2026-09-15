# Healthcare Backend API

A Django + Django REST Framework backend for managing patients, doctors, and patient-doctor
assignments, with JWT-based authentication and PostgreSQL as the data store.

## Tech Stack

- Django + Django REST Framework
- PostgreSQL
- djangorestframework-simplejwt (JWT authentication)
- python-decouple (environment variable management)

## Project Structure

```
healthcare_api/
├── accounts/       # Custom user model, register/login
├── patients/        # Patient CRUD, scoped to the creating user
├── doctors/          # Doctor CRUD, shared across all users
├── mappings/       # Patient-doctor assignment
└── healthcare_api/  # Project settings, root urls.py
```

## Setup

### 1. Clone and create a virtual environment

```bash
git clone <repo-url>
cd healthcare_api
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your own values:

```bash
cp .env.example .env
```

```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Create the PostgreSQL database

```bash
createdb healthcare_db
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Start the server

```bash
python manage.py runserver
```

The API is now available at `http://localhost:8000/api/`.

## Authentication

All patient, doctor, and mapping endpoints require a JWT access token in the request header:

```
Authorization: Bearer <access_token>
```

Get a token pair by logging in (see below). Access tokens expire after 60 minutes; use the
refresh token to get a new one via simplejwt's `/api/auth/login/refresh/` if enabled.

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| POST | `/api/auth/register/` | Register a new user (name, email, password) | No |
| POST | `/api/auth/login/` | Log in, returns JWT access + refresh tokens | No |

### Patients

Patients are scoped to the user who created them — you can only view, edit, or delete patients
you added yourself.

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| POST | `/api/patients/` | Add a new patient | Yes |
| GET | `/api/patients/` | List patients you created | Yes |
| GET | `/api/patients/<id>/` | Get a specific patient | Yes |
| PUT | `/api/patients/<id>/` | Update a patient | Yes |
| DELETE | `/api/patients/<id>/` | Delete a patient | Yes |

### Doctors

Doctors are a shared resource — visible to all authenticated users regardless of who created them.

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| POST | `/api/doctors/` | Add a new doctor | Yes |
| GET | `/api/doctors/` | List all doctors | Yes |
| GET | `/api/doctors/<id>/` | Get a specific doctor | Yes |
| PUT | `/api/doctors/<id>/` | Update a doctor | Yes |
| DELETE | `/api/doctors/<id>/` | Delete a doctor | Yes |

### Patient-Doctor Mappings

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to a patient | Yes |
| GET | `/api/mappings/` | List all mappings for your patients | Yes |
| GET | `/api/mappings/<patient_id>/` | List all doctors assigned to a specific patient | Yes |
| DELETE | `/api/mappings/<id>/` | Remove a mapping (unassign a doctor) | Yes |

Note: `GET /api/mappings/<patient_id>/` takes a **patient ID**, not a mapping ID — it returns
every doctor assigned to that patient. `DELETE /api/mappings/<id>/` takes the mapping's own ID.

## Example Requests

**Register**
```json
POST /api/auth/register/
{
  "name": "Shivam",
  "email": "shivam@example.com",
  "password": "strongpassword123"
}
```

**Login**
```json
POST /api/auth/login/
{
  "email": "shivam@example.com",
  "password": "strongpassword123"
}
```

**Create a patient**
```json
POST /api/patients/
Authorization: Bearer <access_token>
{
  "name": "John Doe",
  "age": 45,
  "gender": "M",
  "address": "123 Main St",
  "phone": "9876543210"
}
```

**Assign a doctor to a patient**
```json
POST /api/mappings/
Authorization: Bearer <access_token>
{
  "patient": 1,
  "doctor": 2
}
```

## Notes

- Passwords are validated against Django's built-in password validators (minimum length,
  not fully numeric, not too common).
- A user can only assign doctors to patients they created — attempting to map a doctor to
  someone else's patient returns a validation error.
- The same doctor cannot be assigned to the same patient twice (enforced at the database level).