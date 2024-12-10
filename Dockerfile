# Use the official Python base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app
# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Expose the FastAPI default port
EXPOSE $APP_PORT

CMD ["python", "main.py"]
