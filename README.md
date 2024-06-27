# Commeta Menu Service

## Prerequisites

- Docker
- Docker Compose
- Python (for development)
- FastAPI
- SQLAlchemy
- Alembic

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/murtazox04/commeta-menu-service.git
cd repository
```

## Environment Variables

Create a .env file in the root directory with the following environment variables:

```bash
# PostgreSQL Database
DB_HOST=db
DB_PORT=5432
DB_NAME=menu_service
DB_USER=postgres
DB_PASSWORD=1234
```

## Docker Compose Setup

Build and start the containers using Docker Compose:
```bash
docker-compose up -d --build
```

This command will build the Docker images defined in docker-compose.yml and start the services (api and db).

## Running Migrations

### Alembic

To manage database migrations, we use Alembic. After setting up your Docker containers:

1. Access the `api` service container:

    ```bash
    docker-compose exec api bash
    ```

2. Generate an initial migration (replace `message` with a meaningful description):

    ```bash
    alembic revision --autogenerate -m "message"
    ```
3. Apply the migration to your database:

    ```bash
    alembic upgrade head
    ```

## Stopping the Application

To stop the Docker containers:

```bash
docker-compose down
```

## Additional Notes

- Replace placeholders (`repository`, `message`, etc.) with actual values relevant to your project.
- Customize the Docker configurations (`docker-compose.yml`, `Dockerfile`) as needed for your specific requirements.
- Ensure proper security practices when handling sensitive information such as database passwords.
- For production deployment, consider using environment-specific configurations and settings.