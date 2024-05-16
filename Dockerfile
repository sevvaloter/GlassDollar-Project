# Use official Python image
    FROM python:3.9

    # Set the working directory
    WORKDIR /app

    # Copy requirements.txt and install dependencies
    COPY requirements.txt .
    RUN pip install -r requirements.txt

    # Copy the application code
    COPY . .

    # Expose port 8000 for FastAPI
    EXPOSE 8000

    # Run FastAPI application using Uvicorn
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]