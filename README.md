# Fastapi Service

---
## Python Run
Set up and run the FastAPI service in your local environment. 
> This process involves creating a virtual environment, installing dependencies, and starting the FastAPI service.

#### init env
- python3 -m venv app/venv
- source app/venv/bin/activate
- pip3 install --upgrade pip
- pip3 install --no-cache-dir -r build/requirements.txt

#### prepare dependencies
- redis
- mysql

#### init db (first time only)
- make init_db

#### run
- uvicorn app.main:app --reload

#### test
- http://localhost:8000/api/version

---
## Docker Run
Use Docker to build and run FastAPI services. 
> Docker provides an isolated environment for running your application, ensuring consistent behavior regardless of local environment differences.

#### build docker
- make build_fastapi
- make build_fluentd

#### init db (first time only)
- make init_db

#### start service
- make start

#### stop service
- make stop

#### test
- http://localhost:80/api/version

---
## VENV
venv is a built-in Python module for creating virtual environments.
> A virtual environment is an isolated Python environment that allows you to manage dependencies for each project independently, without affecting the global Python environment.

#### add plug-in
- source app/venv/bin/activate
- pip3 install xyz

#### export plug-in list
- pip3 freeze > build/requirements.txt

#### exit
- deactivate

---
## Test Run

#### test
- make check