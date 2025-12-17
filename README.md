# Library Management System

REST API for managing a library - search books, manage loans, and handle user access.

Built with Django REST Framework and PostgreSQL.

## Overview

This application provides:
- Book catalog with search and filtering
- User authentication via JWT tokens
- Loan management for registered users
- Admin panel for library staff

## Live Demo

| Resource | URL |
|----------|-----|
| **GitHub Repo** | https://github.com/divy551/Library-management-system- |
| **Swagger UI** | https://web-production-f1bce.up.railway.app/swagger/ |
| **ReDoc** | https://web-production-f1bce.up.railway.app/redoc/ |
| **Admin Panel** | https://web-production-f1bce.up.railway.app/admin/ |
| **API Base** | https://web-production-f1bce.up.railway.app/v1/ |

## Requirements

- Python 3.11 or higher
- PostgreSQL database
- pip package manager

## Setup Instructions

```bash
# Clone and navigate to project
git clone <repository-url>
cd library-management
# ... (rest of setup)
```

## Interactive Docs

- **Swagger UI:** `/swagger/`
- **ReDoc:** `/redoc/`
- **Admin Panel:** `/admin/`

## Running Tests

```bash
pytest                    # All tests
pytest -v                 # Verbose
pytest --cov=apps        # With coverage
```

## Docker Usage

```bash
docker-compose up --build
# Available at http://localhost:8001
```

## Deployment

See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for hosting setup.

### Required Environment Variables

| Name | Purpose |
|------|---------|
| SECRET_KEY | Encryption key |
| DEBUG | Set False for production |
| DATABASE_URL | PostgreSQL URL |
| ALLOWED_HOSTS | Domain whitelist |

## Project Layout

```
├── apps/
│   ├── accounts/    # Authentication
│   ├── books/       # Catalog
│   └── loans/       # Borrowing
├── config/          # Settings
├── tests/           # Test suite
└── requirements.txt
```

## Security Measures

- SQL injection protection via ORM
- XSS headers enabled
- CSRF token validation
- Clickjacking prevention

## Tech Stack

- Django 5.x
- Django REST Framework
- PostgreSQL
- JWT (SimpleJWT)
- Swagger (drf-yasg)
- Docker

## License

MIT
