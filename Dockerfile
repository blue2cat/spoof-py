# Use an official Python runtime as the base image
FROM ubuntu:latest

USER root

# Install Python and required packages
RUN apt-get update && apt-get install -y python3 python3-pip iptables

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Enable IP forwarding
RUN echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

# Apply the sysctl changes
RUN sysctl -p

# Copy the rest of the application code into the container
COPY . .

# Set the command to run the application as root
CMD ["python3", "-u", "spoofpy.py"]
