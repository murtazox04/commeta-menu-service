# Commeta Menu Service

A microservice for managing menu-related operations.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/murtazox04/commeta-menu-service.git
   cd commeta-menu-service
2. Create a `.env` file in the root directory with the following content:
   ```bash
   DB_HOST=db
   DB_PORT=5432
   DB_NAME=menu_service
   DB_USER=postgres
   DB_PASSWORD=1234
   ```
3. Build and start the containers:
   ```bash
   docker-compose up -d --build
   ```
4. Enter the docker container:
   ```bash
   docker-compose exec -it menu-admin /bin/sh
   ```
5. Enter the project directory:
   ```bash
   cd admin
   ```
6. Create an admin superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Access the admin panel at `http://localhost:8000/admin`

# Development

## For local development, you'll need:
- Python
- FastAPI
- Django
- Django-Unfold
- SQLAlchemy
- Alembic

## Stopping the Application
To stop and remove the Docker containers:

   ```bash
   docker-compose down
   ```

## Additional Notes

- Customize Docker configurations in docker-compose.yml and Dockerfile as needed.
- For production deployment, use environment-specific configurations and enhanced security practices.
- Refer to individual service documentation for more detailed information.