# Use the official Python slim image as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies and utilities
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    wget \
    unzip \
    # Oracle Instant Client needs this library to work
    libaio1 \  
    && rm -rf /var/lib/apt/lists/*

# Install Oracle Instant Client
RUN wget https://download.oracle.com/otn_software/linux/instantclient/2350000/instantclient-basic-linux.x64-23.5.0.24.07.zip && \
    unzip instantclient-basic-linux.x64-23.5.0.24.07.zip && \
    mv instantclient_23_5 /opt/oracle && \
    rm instantclient-basic-linux.x64-23.5.0.24.07.zip && \
    echo /opt/oracle/instantclient_23_5 > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig

# Copy the application code to the container
COPY . /app

# Install Python dependencies
# RUN pip install --no-cache-dir fastapi sqlalchemy pydantic uvicorn cx_Oracle
RUN pip install --no-cache-dir -r requirements.txt


# Set environment variables for Oracle Instant Client
#Corrected this to include existing LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/opt/oracle:$LD_LIBRARY_PATH  



# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
