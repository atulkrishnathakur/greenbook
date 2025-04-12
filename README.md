# create a project greenbook
## create a directory
```
atul@atul-Lenovo-G570:~$ mkdir greenbook

```

## go into this directory
```
atul@atul-Lenovo-G570:~$ cd greenbook

```

## How to use git tag

1. Reference: https://www.geeksforgeeks.org/git-tags/
2. create git tag. command : `git tag <tagname>`
```
atul@atul-Lenovo-G570:~/greenbook$ git tag 3.0

```
3. How to see git tag. command : `$ git tag`
```
atul@atul-Lenovo-G570:~/greenbook$ git tag

```
4. How to push git tag on github. command: `git push origin <tagname>`
```
atul@atul-Lenovo-G570:~/greenbook$ git push origin 3.0 

```
5. How to delete tag locally. command: `git tag -d <tagname>`
```
atul@atul-Lenovo-G570:~/greenbook$ git tag -d 3.0

```
6. how to delete a tag from a remote repository from github.command : `git push origin --delete <tagname>`
```
atul@atul-Lenovo-G570:~/greenbook$ git push origin --delete 3.0

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

9. Run below command to stop running services. After down all all container will be remove.
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
   Command: `$ docker tag <local image name>:<tag> <docker user name >/<docker repository>:<tag>`
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

2. Create the `greenbook/nginx.conf` file in project root directory to use in docker.
```
events {}

http {
    upstream fastapi_server {
        server fastapiapp:8000; # It is the yml file service name and port
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

## How to go into container

1. run command to go into project in container. command is `$ docker exec -it <container id> /bin/bash`
 
2. see the below examples of commands. In this example you will see `greenbook` directory of project in container. Here `566adae795e7` is the container id.

```
atul@atul-Lenovo-G570:~$ docker exec -it 566adae795e7 /bin/bash
root@566adae795e7:/greenbook# cd ../
root@566adae795e7:/# ls -l
total 60
lrwxrwxrwx   1 root root    7 Feb  3 00:00 bin -> usr/bin
drwxr-xr-x   2 root root 4096 Dec 31 10:25 boot
drwxr-xr-x   5 root root  340 Mar 27 05:01 dev
drwxr-xr-x   1 root root 4096 Mar 27 05:01 etc
drwxr-xr-x   1 root root 4096 Mar 27 05:01 greenbook
drwxr-xr-x   2 root root 4096 Dec 31 10:25 home
lrwxrwxrwx   1 root root    7 Feb  3 00:00 lib -> usr/lib
lrwxrwxrwx   1 root root    9 Feb  3 00:00 lib64 -> usr/lib64
drwxr-xr-x   2 root root 4096 Feb  3 00:00 media
drwxr-xr-x   2 root root 4096 Feb  3 00:00 mnt
drwxr-xr-x   2 root root 4096 Feb  3 00:00 opt
dr-xr-xr-x 328 root root    0 Mar 27 05:01 proc
drwx------   1 root root 4096 Mar 27 05:25 root
drwxr-xr-x   1 root root 4096 Feb  4 05:18 run
lrwxrwxrwx   1 root root    8 Feb  3 00:00 sbin -> usr/sbin
drwxr-xr-x   2 root root 4096 Feb  3 00:00 srv
dr-xr-xr-x  13 root root    0 Mar 27 05:01 sys
drwxrwxrwt   1 root root 4096 Mar 26 04:52 tmp
drwxr-xr-x   1 root root 4096 Feb  3 00:00 usr
drwxr-xr-x   1 root root 4096 Feb  3 00:00 var
root@566adae795e7:/# cd greenbook
root@566adae795e7:/greenbook# ls -l
total 12
drwxr-xr-x 1 root root 4096 Mar 27 05:01 app
drwxr-xr-x 2 root root 4096 Mar 26 04:52 data
-rw-rw-r-- 1 root root   85 Mar 24 05:38 requirements.txt
root@566adae795e7:/greenbook# cd app
root@566adae795e7:/greenbook/app# ls -l
total 8
-rw-rw-r-- 1 root root    0 Mar 26 04:50 __init__.py
drwxr-xr-x 2 root root 4096 Mar 27 05:01 __pycache__
-rw-rw-r-- 1 root root  122 Mar 26 04:52 main.py
root@566adae795e7:/greenbook/app# cd ..
root@566adae795e7:/greenbook# cd data
root@566adae795e7:/greenbook/data# ls -l
total 0
root@566adae795e7:/greenbook/data# exit
exit
atul@atul-Lenovo-G570:~$ 

```

3. press `exit` command to exit from container


## How to use posgressql database and pgadmin4 

1. Take backup first then update the `docker-compose.yml` file forpostgresql database service
```
version: '3.9' # Defines the version of Docker Compose being used

services:
  fastapiapp: # Service for your FastAPI application
    build:
      context: . # Directory containing the Dockerfile
      dockerfile: Dockerfile # Path to the Dockerfile for building the image
    image: fastapiappimage:3.0 # Name and tag for the Docker image
    container_name: fastapiappcontainer # Custom name for the container
    ports:
      - "8000:8000" # Maps port 8000 on the host to port 8000 in the container. Here port map as <hostport>:<containerport>
    volumes:
      - webstore:/greenbook/data # Persistent storage for application-specific data
    env_file: 
      - .env # Load all environment variables from the .env file
    environment:
      - ENV=$ENV # Explicitly defines the ENV variable from the .env file
    depends_on:
      - postgresdb # Ensures PostgreSQL starts before FastAPI app
    networks:
      - greenbooknetwork # Connects to your custom network

  nginx: # Service for the Nginx web server
    image: nginx:stable # Uses the stable version of the official Nginx image
    container_name: nginxcontainer # Custom name for the container
    ports:
      - "80:80" # Maps port 80 on the host to port 80 in the container. Here port map as <hostport>:<containerport>
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro # Mounts the custom Nginx configuration file in read-only mode
    depends_on:
      - fastapiapp # Ensures FastAPI app starts before Nginx
    networks:
      - greenbooknetwork # Connects to your custom network

  postgresdb: # Service for the PostgreSQL database
    image: postgres:17 # Uses the official PostgreSQL image for version 17
    container_name: postgrescontainer # Custom name for the container
    restart: always # Automatically restarts the container if it stops or after a host machine reboot
    env_file: 
      - .env # Load all environment variables from the .env file
    environment:
      - POSTGRES_USER=$POSTGRES_USER # Explicitly defines the POSTGRES_USER and $POSTGRES_USER from the .env file
      - POSTGRES_PASSWORD=$POSTGRES_PASSWORD # Explicitly defines the POSTGRES_PASSWORD and $POSTGRES_PASSWORD from the .env file
      - POSTGRES_DB=$POSTGRES_DB # Explicitly defines the POSTGRES_DB and $POSTGRES_DB from the .env file
      - POSTGRES_SERVER=$POSTGRES_SERVER # Explicitly defines the POSTGRES_SERVER and $POSTGRES_SERVER from the .env file
      - POSTGRES_PORT=$POSTGRES_PORT # Explicitly defines the POSTGRES_PORT and $POSTGRES_PORT from the .env file
    volumes:
      - postgresdata:/var/lib/postgresql/data # Persistent storage for database data
    networks:
      - greenbooknetwork # Connects to your custom network

  pgadmin4: # Service for pgAdmin4
    image: dpage/pgadmin4:9.1.0 # Uses pgAdmin4 version 9.1.0
    container_name: pgadmin4container # Custom name for the pgAdmin4 container
    ports:
      - "5050:80" # Maps port 5050 on the host to port 80 in the container
    environment:
      - PGADMIN_DEFAULT_EMAIL=$PGADMIN_DEFAULT_EMAIL # Admin email for logging into pgAdmin4
      - PGADMIN_DEFAULT_PASSWORD=$PGADMIN_DEFAULT_PASSWORD # Admin password for logging into pgAdmin4
    depends_on:
      - postgresdb # Ensures PostgreSQL starts before pgAdmin4
    networks:
      - greenbooknetwork # Connects to your custom network

volumes:
  webstore: # Named volume for FastAPI app data
    driver: local
    name: greenbook_webstore # Explicitly set the volume name

  postgresdata: # Named volume for PostgreSQL data
    driver: local
    name: greenbook_postgresdata # Explicitly set the volume name

networks:
  greenbooknetwork: # Use consistent naming for the custom network
    driver: bridge
    name: greenbook_network # Explicitly provide network name.
    
```

2. open the `http://localhost:5050` to open pgadmin4 in browser. enter `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD` password to login

3. connect pgadmin4 to use
  - install pgadmin4
  - Right click on Severs
  - Click on Register
  - Click on Server
  - General Tab
    - name: server1
  - Connection Tab
    - Host name/address: postgresdb (Note: PostgreSQL database service name of docker-compose.yml file)
    - Port: 5432
    - Maintenance Database: postgres
    - Username: usergreenbookdb (Note: PostgreSQL database username of docker-compose.yml file)
    - Password: ****** (Note: PostgreSQL database password of docker-compose.yml file)
    - Click on Save button
  - Click on Server1
    - to show all database
  - Right click on server1
    - Click on Create
    - Click on Database (note: you can create database)

4. How to check database in postgresql container
  - run the command: `docker exec -it < container name Or container id > bash`
    ```
    atul@atul-Lenovo-G570:~/greenbook$ docker exec -it postgrescontainer bash
    ```
  - Run below command to login in postgresql database. Command: `psql -U <database user> -d <database name>`
    ```
    root@0e88346bcaf6:/# psql -U usergreenbookdb -d greenbookdb
    psql (17.4 (Debian 17.4-1.pgdg120+2))
    Type "help" for help.

    greenbookdb=#
    ```
    
  - type `\q` to exit from postgresql database
    ```
    greenbookdb=# \q
    ```
  - type `exit` to exit from container
    ```
    root@0e88346bcaf6:/# exit
    ``` 
## How to write `docker-compose.yml` that if reboot the system
1. first run the command to run `docker-compose.yml` file
```
atul@atul-Lenovo-G570:~/greenbook$ docker compose up -d --build
```
2.  If you are using `restart: always` in services then docker container will be automatically start when system reboot.
```
version: '3.9' # Defines the version of Docker Compose being used

services:
  fastapiapp: # Service for your FastAPI application
    build:
      context: . # Directory containing the Dockerfile
      dockerfile: Dockerfile # Path to the Dockerfile for building the image
    image: fastapiappimage:4.0 # Name and tag for the Docker image
    container_name: fastapiappcontainer # Custom name for the container
    ports:
      - "8000:8000" # Maps port 8000 on the host to port 8000 in the container. Here port map as <hostport>:<containerport>
    volumes:
      - webstore:/greenbook/data # Persistent storage for application-specific data
    env_file: 
      - .env # Load all environment variables from the .env file
    environment:
      - ENV=$ENV # Explicitly defines the ENV variable from the .env file
    depends_on:
      - postgresdb # Ensures PostgreSQL starts before FastAPI app
    networks:
      - greenbooknetwork # Connects to your custom network
    restart: always # Automatically restarts the container if it stops or after a host machine reboot

  nginx: # Service for the Nginx web server
    image: nginx:stable # Uses the stable version of the official Nginx image
    container_name: nginxcontainer # Custom name for the container
    ports:
      - "80:80" # Maps port 80 on the host to port 80 in the container. Here port map as <hostport>:<containerport>
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro # Mounts the custom Nginx configuration file in read-only mode
    depends_on:
      - fastapiapp # Ensures FastAPI app starts before Nginx
    networks:
      - greenbooknetwork # Connects to your custom network
    restart: always # Automatically restarts the container if it stops or after a host machine reboot

  postgresdb: # Service for the PostgreSQL database
    image: postgres:17 # Uses the official PostgreSQL image for version 17
    container_name: postgrescontainer # Custom name for the container
    env_file: 
      - .env # Load all environment variables from the .env file
    environment:
      - POSTGRES_USER=$POSTGRES_USER # Explicitly defines the POSTGRES_USER and $POSTGRES_USER from the .env file
      - POSTGRES_PASSWORD=$POSTGRES_PASSWORD # Explicitly defines the POSTGRES_PASSWORD and $POSTGRES_PASSWORD from the .env file
      - POSTGRES_DB=$POSTGRES_DB # Explicitly defines the POSTGRES_DB and $POSTGRES_DB from the .env file
      - POSTGRES_SERVER=$POSTGRES_SERVER # Explicitly defines the POSTGRES_SERVER and $POSTGRES_SERVER from the .env file
      - POSTGRES_PORT=$POSTGRES_PORT # Explicitly defines the POSTGRES_PORT and $POSTGRES_PORT from the .env file
    volumes:
      - postgresdata:/var/lib/postgresql/data # Persistent storage for database data
    networks:
      - greenbooknetwork # Connects to your custom network
    restart: always # Automatically restarts the container if it stops or after a host machine reboot

  pgadmin4: # Service for pgAdmin4
    image: dpage/pgadmin4:9.1.0 # Uses pgAdmin4 version 9.1.0
    container_name: pgadmin4container # Custom name for the pgAdmin4 container
    ports:
      - "5050:80" # Maps port 5050 on the host to port 80 in the container
    environment:
      - PGADMIN_DEFAULT_EMAIL=$PGADMIN_DEFAULT_EMAIL # Admin email for logging into pgAdmin4
      - PGADMIN_DEFAULT_PASSWORD=$PGADMIN_DEFAULT_PASSWORD # Admin password for logging into pgAdmin4
    depends_on:
      - postgresdb # Ensures PostgreSQL starts before pgAdmin4
    networks:
      - greenbooknetwork # Connects to your custom network
    restart: always # Automatically restarts the container if it stops or after a host machine reboot

volumes:
  webstore: # Named volume for FastAPI app data
    driver: local
    name: greenbook_webstore # Explicitly set the volume name

  postgresdata: # Named volume for PostgreSQL data
    driver: local
    name: greenbook_postgresdata # Explicitly set the volume name

networks:
  greenbooknetwork: # Use consistent naming for the custom network
    driver: bridge
    name: greenbook_network # Explicitly provide network name.
```

## How to create alembic in `greenbook/app` directory of project
```
(venv) atul@atul-Lenovo-G570:~/greenbook/app$ alembic init alembic

```

## How to install package from `requirements.txt`
```
(venv) atul@atul-Lenovo-G570:~/greenbook$ pip install -r requirements.txt

```


## How to create a nginx configuration file in project root directory to run in local machine
1. create `greenbook/nginx-dev.conf` file
```
events {}

http {
    upstream fastapi_server {
       server localhost:8000; # for development on local machine
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

2. Run the below command. Use the -c option to point nginx to your custom nginx-dev.conf file
```
atul@atul-Lenovo-G570:~/greenbook$ sudo nginx -c /home/atul/greenbook/nginx-dev.conf
```
3. If you want to completely stop nginx from your custom configuration.
```
(venv) atul@atul-Lenovo-G570:~/greenbook$ sudo nginx -s stop
```
4. Restart the nginx
```
atul@atul-Lenovo-G570:~/greenbook$ sudo systemctl restart nginx
```


# How to set valume from `.yml` file
```
version: '3.9' # Defines the version of Docker Compose being used

services:
  fastapiapp: # Service for your FastAPI application
    build:
      context: . # Directory containing the Dockerfile
      dockerfile: Dockerfile # Path to the Dockerfile for building the image
    image: fastapiappimage:7.0 # Name and tag for the Docker image
    container_name: fastapiappcontainer # Custom name for the container
    ports:
      - "8000:8000" # Maps port 8000 on the host to port 8000 in the container. Here port map as <hostport>:<containerport>
    volumes:
      - webstore:/greenbook/data # Persistent storage for application-specific data
    env_file: 
      - .env # Load all environment variables from the .env file
    environment:
      - ENV=$ENV # Explicitly defines the ENV variable from the .env file
    depends_on:
      - postgresdb # Ensures PostgreSQL starts before FastAPI app
    networks:
      - greenbooknetwork # Connects to your custom network
    restart: always # Automatically restarts the container if it stops or after a host machine reboot

  nginx: # Service for the Nginx web server
    image: nginx:stable # Uses the stable version of the official Nginx image
    container_name: nginxcontainer # Custom name for the container
    ports:
      - "80:80" # Maps port 80 on the host to port 80 in the container. Here port map as <hostport>:<containerport>
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro # Mounts the custom Nginx configuration file in read-only mode. It is bind mount. It is not persistent valume
    depends_on:
      - fastapiapp # Ensures FastAPI app starts before Nginx
    networks:
      - greenbooknetwork # Connects to your custom network
    restart: always # Automatically restarts the container if it stops or after a host machine reboot

  postgresdb: # Service for the PostgreSQL database
    image: postgres:17 # Uses the official PostgreSQL image for version 17
    container_name: postgrescontainer # Custom name for the container
    env_file: 
      - .env # Load all environment variables from the .env file
    environment:
      - POSTGRES_USER=$POSTGRES_USER # Explicitly defines the POSTGRES_USER and $POSTGRES_USER from the .env file
      - POSTGRES_PASSWORD=$POSTGRES_PASSWORD # Explicitly defines the POSTGRES_PASSWORD and $POSTGRES_PASSWORD from the .env file
      - POSTGRES_DB=$POSTGRES_DB # Explicitly defines the POSTGRES_DB and $POSTGRES_DB from the .env file
      - POSTGRES_SERVER=$POSTGRES_SERVER # Explicitly defines the POSTGRES_SERVER and $POSTGRES_SERVER from the .env file
      - POSTGRES_PORT=$POSTGRES_PORT # Explicitly defines the POSTGRES_PORT and $POSTGRES_PORT from the .env file
    volumes:
      - postgresdata:/var/lib/postgresql/data # Persistent storage for database data
    networks:
      - greenbooknetwork # Connects to your custom network
    restart: always # Automatically restarts the container if it stops or after a host machine reboot

  pgadmin4: # Service for pgAdmin4
    image: dpage/pgadmin4:9.1.0 # Uses pgAdmin4 version 9.1.0
    container_name: pgadmin4container # Custom name for the pgAdmin4 container
    ports:
      - "5050:80" # Maps port 5050 on the host to port 80 in the container
    environment:
      - PGADMIN_DEFAULT_EMAIL=$PGADMIN_DEFAULT_EMAIL # Admin email for logging into pgAdmin4
      - PGADMIN_DEFAULT_PASSWORD=$PGADMIN_DEFAULT_PASSWORD # Admin password for logging into pgAdmin4
    depends_on:
      - postgresdb # Ensures PostgreSQL starts before pgAdmin4
    volumes:
      - pgadmin4data:/var/lib/pgadmin # Persistent storage for database data
    networks:
      - greenbooknetwork # Connects to your custom network
    restart: always # Automatically restarts the container if it stops or after a host machine reboot

volumes:
  webstore: # Named volume for FastAPI app data
    driver: local # used to create valume in host machine
    name: greenbook_webstore # Explicitly set the volume name

  postgresdata: # Named volume for PostgreSQL data
    driver: local # used to create valume in host machine
    name: greenbook_postgresdata # Explicitly set the volume name

  pgadmin4data: # Named volume for PostgreSQL data
    driver: local # used to create valume in host machine
    name: greenbook_pgadmin4data # Explicitly set the volume name

networks:
  greenbooknetwork: # Use consistent naming for the custom network
    driver: bridge
    name: greenbook_network # Explicitly provide network name.
```
## How to check volume in host machine
1. In host machine you can see volume path `/var/lib/docker/volumes/<volume_name>`

## How to import `.sql ` file form web pgadmin4
1. Copy and paste `.sql` file in docker volume. Path in host machine `/var/lib/docker/volumes/greenbook_pgadmin4data/_data/storage/a***a@gmail.com/`. In `yml` file you can see `pgadmin4data:/var/lib/pgadmin`.
2. login in container and check the path `/var/lib/pgadmin` because in yml file you can see `pgadmin4data:/var/lib/pgadmin`.
3. open the `http://localhost:5050`
4. login in web pgadmin4
5. write clikc on database and click on query tool. Click on open file then you will see your pasted file. Select your file and click on open button. Click on run button to execute queries of `.sql` file.

## Where file will be save after export from web pgadmin4
1. Your exported file will be save in volume. Path of volume in host machine is `/var/lib/docker/volumes/greenbook_pgadmin4data/_data/storage/a***a_gmail.com/`

## How to check pgadmin4 container
1. first login in pgadmin4 container
```
atul@atul-Lenovo-G570:~$ docker exec -it pgadmin4container /bin/bash

```
2. In container to check exported sql file `/var/lib/pgadmin/storage/a*****a_gmail.com`. In yml file you can see `pgadmin4data:/var/lib/pgadmin`
```
0a0a6a8eb77d:/var/lib/pgadmin/storage/a*****a_gmail.com$ ls -l
total 32
-rw-rw-r--    1 root     root         21893 Apr  4 04:46 greenbook3.sql
-rw-r--r--    1 pgadmin  root          1095 Apr 10 06:20 postgres.sql
-rw-r--r--    1 pgadmin  root          1095 Apr 11 05:30 postgresbkp.sql

```

## How to check env in container
command: `atul@atul-Lenovo-G570:~$ docker exec -it <container name or id> env`
```
atul@atul-Lenovo-G570:~$ docker exec -it fastapiappcontainer env

```