### Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory to /app
WORKDIR /app

# Install vim
RUN apt-get update && apt-get install -y vim && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . .


# Make port 5000 available to the world outside this container
# in app.py, the port number should be the same as this, and so does the command option -p for running container
EXPOSE 5000

# Define environment variable
#ENV NAME World

# Run app.py when the container launches
CMD gunicorn --bind 0.0.0.0:5000 app:app

