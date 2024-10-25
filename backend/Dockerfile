# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    mariadb-client \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install requests
RUN pip install -q -U google-generativeai
RUN pip install django-cors-headers
RUN pip install python-dotenv

# Copy the current directory contents into the container at /code
COPY . /code/

# Run migrations and start the Django development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
