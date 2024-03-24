# Use a base image with MongoDB pre-installed
FROM mongo:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY Bot/ /app/

# Install any necessary dependencies for the Python script
RUN apt-get update && \
    apt install -y python3 && \
    apt install -y pip

RUN pip install -r /app/requirements.txt

# Set the command to run the Python script when the container starts
CMD ["python3", "CarRatingBot.py"]
