# Technology Stack & Build System

## Backend Stack

- **Framework**: FastAPI with Uvicorn ASGI server
- **Database**: PostgreSQL 15 with SQLModel ORM and Alembic migrations
- **Cache/Sessions**: Redis 7
- **Authentication**: JWT tokens with python-jose, bcrypt password hashing
- **Python Version**: 3.9+

## Frontend Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite 4
- **Styling**: Tailwind CSS 3
- **HTTP Client**: Axios with TanStack Query for state management
- **Routing**: React Router DOM 6
- **Node Version**: 18+

## Infrastructure

- **Web Server**: Nginx (reverse proxy and static file serving)
- **Containerization**: Docker with Docker Compose
- **Database**: PostgreSQL with connection pooling
- **System Services**: SSH daemon with custom configuration
- **Process Management**: Systemd (in containers)

## Development Tools

- **Package Manager**: uv for Python package and virtual environment management
- **Python**: pytest, ruff (linting/formatting), mypy, pre-commit
- **JavaScript**: ESLint, Prettier, Vitest, Testing Library
- **Database**: SQLModel for ORM, Alembic for migrations, psycopg2 for PostgreSQL connectivity

## Common Commands

### Development Environment
```bash
# Start full development stack
make dev-up

# Stop development environment  
make dev-down

# View logs
make dev-logs

# Get shell access to pubnix container
make dev-shell

# First-time setup
make setup-dev
```

### Testing
```bash
# Run all tests
make test

# Unit tests only
make test-unit

# Integration tests only  
make test-integration

# Test SSH connection
make ssh-test
```

### Code Quality
```bash
# Lint all code
make lint

# Format all code
make format

# Backend only
cd backend && uv run ruff check . && uv run ruff format .

# Frontend only
cd web && npm run lint && npm run format
```

### Database
```bash
# Database migrations (backend directory)
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "description"

# Initialize database with test data
uv run python init_db.py
```

### Docker Management
```bash
# Build all images
make build

# Clean up containers and volumes
make clean
```

## Port Configuration

- **SSH**: 2222 (dev) / 22 (prod)
- **Web Interface**: 8080 (nginx)
- **HTTPS**: 8443 (dev)
- **Frontend Dev Server**: 3000 (Vite)
- **Database**: 5432 (PostgreSQL)
- **Cache**: 6379 (Redis)

## Environment Variables

- `PUBNIX_ENV`: development/production
- `PUBNIX_DEBUG`: true/false
- `PUBNIX_LOG_LEVEL`: DEBUG/INFO/WARNING/ERROR
- `NODE_ENV`: development/production
- `VITE_API_URL`: Frontend API endpoint