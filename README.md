# Fastapi Service
## Docker Run

### build docker
* make docker

### start service
* make start

### stop service
* make stop

## VENV

### init
* cd app
* python3 -m venv venv
* source venv/bin/activate
* pip3 install --upgrade pip
* pip3 install -r ../build/requirements.txt

### add plug-in
* cd app
* source venv/bin/activate
* pip3 install xyz

### export plug-in list
* pip freeze > requirements.txt

### exit
deactivate


