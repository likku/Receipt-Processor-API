FROM python:3.12

# Setting up the working dir
WORKDIR /app

# Copying contents to WD
COPY . /app

# Using the req file
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 1000

# Defining env variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run Flask when start
CMD ["flask", "run"]
