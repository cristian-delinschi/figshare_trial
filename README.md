# Accounts App Manager


## Endpoints

<img width="1451" alt="Screenshot 2024-08-26 at 13 19 14" src="https://github.com/user-attachments/assets/5c040f09-e71f-4d78-b822-9509f406ca10">


## Jenkins
https://github.com/user-attachments/assets/2aba2a4e-c555-4a73-b5a7-32b9d8f372c0

## Github Login
https://github.com/user-attachments/assets/7064b1d1-ec32-4f50-82aa-11bf2b61e42a

#### Features

- [x] Authorization and authentication with JWT (JSON Web Token)
- [x] Protected Endpoints
- [x] Email Validation
- [x] Use of Hashed passwords
- [x] Jenkins Job that builds the docker image when a GitHub commit happens on the main branch

#### Technologies used

- FastAPI
- Maria DB
- SqlAlchemy
- Docker

#### Dockerized App

```sh
docker-compose up --build
```

#### Set Up Local Env

```sh
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Set ngrok for local Jenkins

```sh
ngrok http 8080
```

#### Run tests

```sh
pytest -s tests
```
