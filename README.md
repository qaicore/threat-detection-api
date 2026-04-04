# Threat Detection API

A threat intelligence and case management REST API built with FastAPI, PostgreSQL, and Docker. Built as part of a security engineering portfolio — simulates the kind of API used by SOC analysts to track threat indicators and manage incident cases.

---

## Tech Stack

- **FastAPI** — Python web framework
- **PostgreSQL 15** — database
- **SQLAlchemy** — ORM
- **JWT (python-jose)** — authentication
- **Docker + Docker Compose** — containerization
- **pytest** — testing

---

## Running the Project

### Prerequisites
- Docker Desktop installed and running

### Start the API

```bash
docker-compose up --build
```

API will be available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

### Stop the API

```bash
docker-compose down
```

---

## Environment Variables

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://postgres:<your_password>@db:5432/threats
SECRET_KEY=<your_secret_key>
ALGORITHM=HS256
POSTGRES_PASSWORD=<your_password>
POSTGRES_DB=threats
```

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Authentication

This API uses JWT Bearer token authentication.

### Register
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "analyst@company.com", "password": "yourpassword"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "analyst@company.com", "password": "yourpassword"}'
```

Returns a JWT token. Use it in subsequent requests:

```bash
curl -H "Authorization: Bearer <your_token>" http://localhost:8000/api/indicators
```

### Swagger UI

The `/docs` page requires curl or a REST client (Postman, Insomnia) for authenticated requests. Login via `POST /auth/login`, copy the `access_token`, and pass it as a Bearer token in the Authorization header.

---

## Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create analyst account |
| POST | `/auth/login` | Get JWT token |

### Indicators
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/indicators` | Submit a threat indicator |
| GET | `/api/indicators` | List all indicators (filterable, paginated) |
| GET | `/api/indicators/{id}` | Get specific indicator |

**Query params for GET /api/indicators:**
- `?type=IP` — filter by type
- `?severity=HIGH` — filter by severity
- `?skip=0&limit=10` — pagination

### Cases
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/cases` | Create an incident case |
| GET | `/api/cases` | List all cases |
| GET | `/api/cases/{id}` | Get specific case |
| PATCH | `/api/cases/{id}/status` | Update case status |
| POST | `/api/cases/{id}/indicators` | Link an indicator to a case |

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |

---

## Example: Full Workflow

```bash
# 1. Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "analyst@company.com", "password": "password123"}'

# 2. Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "analyst@company.com", "password": "password123"}'

# 3. Submit indicator (use token from login)
curl -X POST http://localhost:8000/api/indicators \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"type": "IP", "value": "203.0.113.45", "severity": "HIGH", "notes": "Seen in 47 failed SSH attempts"}'

# 4. Create case
curl -X POST http://localhost:8000/api/cases \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title": "Server X under attack", "description": "Brute force attempt", "severity": "HIGH"}'

# 5. Link indicator to case
curl -X POST http://localhost:8000/api/cases/1/indicators \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"indicator_id": 1}'

# 6. Close the case
curl -X PATCH http://localhost:8000/api/cases/1/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"status": "CLOSED"}'
```

---

## Running Tests

```bash
# Activate virtual environment (Windows)
venv\Scripts\Activate.ps1

# Run tests
python -m pytest tests/ -v
```

Tests use an in-memory SQLite database — no Docker required for testing.

---

## Project Structure

```
02-incident-case-api/
├── main.py           # FastAPI app, all routes
├── models.py         # SQLAlchemy models
├── schemas.py        # Pydantic schemas
├── database.py       # DB connection and session
├── auth.py           # JWT and password utilities
├── routers/
│   ├── indicators.py
│   └── cases.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_indicators.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```