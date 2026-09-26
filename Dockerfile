# Dockerfile for Flask REST API application

# The base image is set to python:3.14.7, which means that the Docker image will be built on top of the official Python 3.14.7 image. This image includes the Python interpreter and standard libraries, providing a suitable environment for running Python applications.
FROM python:3.14.7

# The EXPOSE instruction is used to inform Docker that the container will listen on port 5000. This allows other containers or services to communicate with the Flask application running inside the container on this port.
# EXPOSE 5000         # not required while using 'gunicorn', it uses port 80 by default, but you can specify a different port if needed.

# The WORKDIR instruction sets the working directory inside the container to /app. This means that any subsequent commands, such as COPY or RUN, will be executed relative to this directory. It also helps organize the application files within the container.
WORKDIR /app


# RUN pip install flask
# COPY . .

# The COPY instruction is used to copy the requirements.txt file from the host machine to the current working directory (/app) inside the container. This allows the container to have access to the necessary dependencies specified in the requirements.txt file.
COPY requirements.txt . 

# The RUN instruction is used to execute the pip install command inside the container, which installs the dependencies listed in the requirements.txt file. This ensures that all required Python packages are available for the Flask application to run correctly.
# RUN pip install -r requirements.txt      # without 'gunicorn'
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# The COPY instruction is used to copy the entire contents of the current directory on the host machine (.) to the current working directory (/app) inside the container. This includes all application files, such as Python scripts, templates, and static assets, allowing the Flask application to be fully available within the container.
COPY . .

# The CMD instruction specifies the command that will be executed when the container is started. In this case, it runs the Flask application using the flask run command, with the --host option set to

# without 'gunicorn'
# CMD ["flask", "run", "--host", "0.0.0.0"]

# with 'gunicorn'
CMD ["gunicorn", "--bind", "0.0.0.0:80", "StoreApp.main:create_app()"]