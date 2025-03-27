# create a project greenbook
## create a directory
```
atul@atul-Lenovo-G570:~$ mkdir greenbook

```

## go into this directory
```
atul@atul-Lenovo-G570:~$ cd greenbook

```


## How to use docker in this project
1. go into the project root directory
2. create docker file
```
atul@atul-Lenovo-G570:~/greenbook$ touch Dockerfile

```

3. manually write below code in dockerfile
```
# Use the official Python image
FROM python:3.12.8

# Set the working directory
WORKDIR /greenbook

# This command put requirements.txt in container in specific directory
COPY ./requirements.txt /greenbook/requirements.txt


# This command will install dependancies in docker container
RUN pip install --no-cache-dir --upgrade -r /greenbook/requirements.txt

# copy source code files and directory in docker container
COPY ./app /greenbook/app

# this is default command. It will run after container start
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

```

4. create a `requirements.txt` file in project root directory and write below code in requirements.txt file

```
fastapi==0.115.11
uvicorn==0.34.0
pydantic==2.10.6
httpx==0.28.1
python-dotenv==1.0.1

```

5. create a `.dockerignore` file and write below code

 - Note: Here I write .env in docker ingnore file because If you do not write in docker ignore file then your credentials will be write in image and your env data will be unsecure.

```
# Ignore environment and configuration files
.env

# Ignore version control directories
.git/
.gitignore

```

6. How to check docker compose version
```
atul@atul-Lenovo-G570:~/greenbook$ docker compose version

```

7. create `docker-compose.yml` in project root directory. and write below code in this file.

```
# This is the version of the Docker Compose file
version: '3.9'

services:
  fastapiapp:
    build:
      context: .
      dockerfile: Dockerfile # Path to the Dockerfile
    image: fastapiappimage:1.0 # Image name and tag
    container_name: fastapiappcontainer # Container name
    ports:
      - "8000:8000" # Mapping container port 8000 to host port 8000
    volumes:
      - webstore:/greenbook/data # Persistent storage for the application
    environment:
      - ENV=production # Set environment variable

volumes:
  webstore:
    driver: local # Use the local driver for storage

```

8. Run the below command to run `docker-compose.yml` file

```
atul@atul-Lenovo-G570:~/greenbook$ docker compose up --build

```
- `--build` flag used to create image and container that is define in `build:` section of `docker-compose.yml` file

- check `http://localhost:8000/docs` in your browser
- but if you close terminal then container will be stop and your application can not be run
- you can press `ctrl-c` to exit


8. Run the below command to run `docker-compose.yml` file container in Detached Mode. If you want to run container in background then use `-d` flag

```
atul@atul-Lenovo-G570:~/greenbook$ docker compose up -d --build

```

9. Run below command to stop running services
```
atul@atul-Lenovo-G570:~/greenbook$ docker compose down

```

10. you can check logs of docker compose

```
atul@atul-Lenovo-G570:~/greenbook$ docker compose logs -f

```

## How to push image in docker hub
1. First create a repository name in docker hub. Reference: https://hub.docker.com/repositories/username
2. create repository in docker hub like `greenbook`
3. login docker in terminal
```
atul@atul-Lenovo-G570:~$ docker login

```
4. Tag your local machine image with this repository.
   Command: `$ docker tag <local image name>:<tag> <docker user name >/<docker repository>:<tag>
   ```
    atul@atul-Lenovo-G570:~$ docker tag fastapiappimage:1.0 atulkrishnathakur/greenbook:1.0

   ```
4. push image on docker
   command: `$ docker push <docker user name>/<docker repository>:<tag>`
   ```
    atul@atul-Lenovo-G570:~$ docker push atulkrishnathakur/greenbook:1.0
   ```
5. Note: when you run `docker images` command then you got `fastapiappimage:1.0` and `atulkrishnathakur/greenbook:1.0` with same image id. It means `atulkrishnathakur/greenbook:1.0` not a new image. It is a simply new reference(tag) of the same image.


## How to use nginx server 
1. edit the docker-compose.yml . Here we are using tag 2.0 in `image: fastapiappimage:2.0`

```
# This is the version of the Docker Compose file
version: '3.9'

services:
  fastapiapp:
    build:
      context: .
      dockerfile: Dockerfile # Path to the Dockerfile
    image: fastapiappimage:2.0 # Image name and tag
    container_name: fastapiappcontainer # Container name
    ports:
      - "8000:8000" # Mapping container port 8000 to host port 8000
    volumes:
      - webstore:/greenbook/data # Persistent storage for the application
    environment:
      - ENV=production # Set environment variable

  nginx:
    image: nginx:stable
    container_name: nginxcontainer
    ports:
      - "80:80" # Map host port 80 to Nginx container port 80
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro # Mount custom Nginx configuration
    depends_on:
      - fastapiapp # Ensure FastAPI app starts before Nginx

volumes:
  webstore:
    driver: local # Use the local driver for storage

```

2. Create the `nginx.conf` file in project root directory.
```
events {}

http {
    upstream fastapi_server {
        server fastapiapp:8000; # Reference the FastAPI service name and port
    }

    server {
        listen 80;

        location / {
            proxy_pass http://fastapi_server;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}

```

