FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install dependencies

# Install the application dependencies.
WORKDIR /app
COPY . .
RUN uv sync --frozen --no-cache


# Command to run the application
# CMD [".venv/bin/fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]
CMD ["uv", "run", "fastapi", "dev", "main.py", "--port", "8000", "--host", "0.0.0.0"]
