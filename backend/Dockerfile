FROM python:3.10-slim

# Set working dir inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything into the container
COPY ./app /app/app

# Run uvicorn from inside the nested /app/app folder
CMD ["uvicorn", "app.__main__:app", "--host", "0.0.0.0", "--port", "8000"]
