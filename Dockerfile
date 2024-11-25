FROM python:3.12

# Setting up the working dir
WORKDIR /app

# Copying contents to WD
COPY . /app

# Using the req file
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Set the default command to run Flask with the specified host and port
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]