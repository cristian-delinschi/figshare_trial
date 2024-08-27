Simple Back-End CRUD application that manages “accounts”.

Endpoints

IMAGE HERE

Features

- > Authorization and authentication with JWT (JSON Web Token)
- > Protected Endpoints
- > Email Validation
- > Use of Hashed passwords

Technologies used

- > FastAPI
- > Maria DB
- > SqlAlchemy
- > Docker

use app from docker

- > docker-compose up --build

use app on local env

- > virtualenv .venv
- > source .venv/bin/activate
- > pip install -r requirements.txt
- > alembic upgrade head
- > uvicorn app.main:app --reload

run tests

- > pytest -s tests

-> testing purposes
