FROM mysql:5.6

# Set working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get -y update && apt-get -y install python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install --trusted-host pypi.python.org -r  requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["python3", "./website/manage.py", "runserver"]
