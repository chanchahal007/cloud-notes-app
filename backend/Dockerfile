FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy the *contents* of the app folder, not the folder itself
COPY app ./app

ENV PYTHONPATH=/app

# ✅ Uvicorn runs from top-level /app and finds app.main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
