#Use python 3.12-slim as base image
FROM python:3.12-slim

#Set the working directory
WORKDIR /app

#Copy the requirements file to the container
COPY requirements.txt .

#Install the dependencies
RUN pip install -r requirements.txt

#Copy the rest of the application code to the container
COPY . /app

#Set the command to run the application
CMD ["python", "app.py"]

#Expose the port the app runs on
EXPOSE 8000