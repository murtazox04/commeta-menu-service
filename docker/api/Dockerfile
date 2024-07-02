# Use the official Python image.
FROM python:3.10

# Set the working directory in the container.
WORKDIR /app

# Copy the dependencies file to the working directory.
COPY ./poetry.lock ./pyproject.toml ./

# Install dependencies.
RUN apt-get update && apt-get install -y build-essential && pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy the rest of the application code to the working directory.
COPY . .

# Ensure alembic.ini is included
COPY ./alembic.ini ./

# Make the entrypoint script executable.
RUN chmod +x ./docker/api/apientry.sh

# Command to run the application.
ENTRYPOINT ["./docker/api/apientry.sh"]
