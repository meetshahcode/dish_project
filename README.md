# Dish Project

A FastAPI-based backend for managing dishes, users, and health endpoints, using PostgreSQL and Redis.

## Setup Instructions

### Prerequisites

- Python 3.9+
- Docker & Docker Compose

### Local Development

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd dish_project
   ```

2. **Create a `.env` file**
3. **Install dependencies**

   ```bash
   uv sync
   ```

4. **Start PostgreSQL and Redis using Docker Compose**

   ```bash
   docker-compose up -d
   ```

5. **Run database migrations**

   ```bash
   alembic upgrade head
   ```

6. **Start the application**

   ```bash
   uvicorn main:app --reload
   ```

   Or, using the provided Dockerfile:

   ```bash
   docker build -t dish-project .
   docker run --env-file .env -p 8000:8000 dish-project
   ```

### Running with Docker Compose (optional)

Uncomment the `app` service in `docker-compose.yml` and adjust environment variables as needed, then run:

```bash
docker-compose up --build
```

## Decisions & Trade-offs

- **Async SQLAlchemy**: Chosen for non-blocking DB operations, improving scalability for concurrent requests.
- **FastAPI**: Selected for its speed, async support, and automatic OpenAPI docs.
- **Dockerized Services**: PostgreSQL and Redis are run in containers for easy setup and isolation.
- **Dependency Management**: Uses `uv` for fast installs and reproducible environments.
- **Configuration**: Managed via Pydantic settings and `.env` files for flexibility and security.
- **Not using ORM auto-migrations**: Alembic is used for explicit DB migrations, providing more control.
- **No frontend**: This project is backend-only, focusing on API endpoints.

## Notes

- Ensure all environment variables are set in `.env` before running.
- For production, review and adjust security settings (e.g., secret keys, allowed hosts).
- The Dockerfile uses `uv` for dependency management; ensure compatibility with your workflow.

---

## Project Structure

```
dish_project/
├── apps/
│   ├── dish/
│   │   ├── models.py        # SQLAlchemy models for dishes
│   │   ├── route.py         # FastAPI routes for dish endpoints
│   │   └── schema.py        # Pydantic schemas for dish API
│   ├── health/
│   │   └── route.py         # Health check and root endpoints
│   └── user/
│       ├── jwt.py           # JWT token utilities and authentication
│       ├── models.py        # SQLAlchemy models for users and blacklist tokens
│       ├── route.py         # FastAPI routes for user/auth endpoints
│       ├── schema.py        # Pydantic schemas for user API
│       └── utils.py         # Utility functions (e.g., UTC timestamp)
├── migration/
│   ├── versions/            # Alembic migration scripts
│   ├── env.py               # Alembic migration environment config
│   ├── script.py.mako       # Alembic migration script template
│   └── README               # Alembic migration readme
├── .env                     # Environment variables for local/dev
├── .gitignore               # Git ignore rules
├── .dockerignore            # Docker ignore rules
├── .python-version          # Python version for pyenv
├── alembic.ini              # Alembic configuration file
├── config.py                # Pydantic settings for app configuration
├── database.py              # SQLAlchemy async DB setup and base class
├── Dockerfile               # Docker build instructions
├── docker-compose.yml       # Docker Compose services (Postgres, Redis, app)
├── exceptions.py            # Custom FastAPI exception classes
├── fast.py                  # FastAPI app instance
├── main.py                  # Main entrypoint, includes routers and middleware
├── pyproject.toml           # Project metadata and dependencies
├── README.md                # Project documentation (this file)
├── utils.py                 # Password hashing utilities
└── uv.lock                  # Lock file for dependencies (managed by uv)
```

### Folder & File Purpose

- **apps/**: Main application code, organized by feature (dish, user, health).
  - **dish/**: All logic related to dish management (models, API, schemas).
  - **user/**: User authentication, models, JWT, and related utilities.
  - **health/**: Health check and root endpoints.
- **migration/**: Database migration scripts and Alembic configuration.
  - **versions/**: Individual migration scripts (auto-generated).
  - **env.py, script.py.mako, README**: Alembic setup and templates.
- **.env**: Environment variables for configuration (never commit secrets).
- **.gitignore, .dockerignore**: Ignore rules for Git and Docker.
- **.python-version**: Python version pinning for development.
- **alembic.ini**: Alembic migration tool configuration.
- **config.py**: Centralized app configuration using Pydantic.
- **database.py**: Async SQLAlchemy engine/session setup and base model.
- **Dockerfile**: Instructions to build the app Docker image.
- **docker-compose.yml**: Multi-service orchestration (Postgres, Redis, app).
- **exceptions.py**: Custom exception classes for consistent API errors.
- **fast.py**: FastAPI app instance (imported by main.py).
- **main.py**: Application entrypoint, includes routers and middleware.
- **pyproject.toml**: Project metadata and dependency specification.
- **README.md**: Project documentation and instructions.
- **utils.py**: Utility functions (e.g., password hashing).
- **uv.lock**: Dependency lock file for reproducible installs.

This structure separates concerns, supports scalability, and makes the codebase easy to navigate and maintain.


