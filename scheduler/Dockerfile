# Use Python 3.11.8 as the base image
FROM python:3.11.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Update package listings and install vim (optional, remove if not needed)
RUN apt-get update && apt-get install -y vim
RUN apt-get install libgomp1
# Install the dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Start a shell to run scripts on-demand, or specify a default command
CMD ["/bin/bash"]
