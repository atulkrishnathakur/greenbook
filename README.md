# create a project greenbook
## create a directory
```
atul@atul-Lenovo-G570:~$ mkdir greenbook

```

## go into this directory
```
atul@atul-Lenovo-G570:~$ cd greenbook

```

## create a readme.md file
```
atul@atul-Lenovo-G570:~/greenbook$ touch README.md

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