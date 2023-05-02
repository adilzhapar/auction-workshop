# pull official base image
FROM python:3.11.2-alpine

# Create a non-root user
RUN adduser -D nonroot

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Set the ownership of the application code to the non-root user
RUN chown -R nonroot /usr/src/app

# Switch to the non-root user
USER nonroot

# Start the application
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8080" ]
