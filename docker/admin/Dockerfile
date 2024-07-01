# Use the official Python image.
FROM python:3.10

# Set the working directory in the container.
WORKDIR ./app

# Copy the dependencies file to the working directory.
COPY ./admin/poetry.lock ./admin/pyproject.toml ./

# Install dependencies.
RUN apt-get update && apt-get install -y build-essential && pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy the rest of the application code to the working directory.
COPY . .

# Make the entrypoint script executable.
RUN chmod +x ./docker/admin/adminentry.sh

# Command to run the application.
ENTRYPOINT ["./docker/admin/adminentry.sh"]
#EXPOSE 8000