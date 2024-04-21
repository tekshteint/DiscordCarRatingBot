# Use a base image with MongoDB pre-installed
FROM mongo:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY . /app/

# Install any necessary dependencies for the Python script
RUN apt-get update && \
   # apt-get upgrade -y && \
    apt install -y python3 && \
    apt install -y pip && \
    apt install -y python3-pip && \
    pip install --upgrade pip && \
    pip install -r /app/Bot/requirements. && \
    apt-get install git -y    

# Set the command to run the Python script when the container starts
CMD ["python3", "CarRatingBot.py"]
