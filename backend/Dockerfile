# backend/Dockerfile
FROM python:3.10

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only the necessary files for installing dependencies
COPY pyproject.toml poetry.lock* /app/

# Disable virtualenv creation and install dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Copy the rest of the application
COPY ruliad /app/ruliad

# Command to run the FastAPI server using Typer
CMD ["python", "-m", "ruliad", "serve"]
