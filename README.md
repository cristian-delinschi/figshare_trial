Simple Back-End CRUD application that manages “accounts”.

<img width="1451" alt="Screenshot 2024-08-26 at 13 19 14" src="https://github.com/user-attachments/assets/5c040f09-e71f-4d78-b822-9509f406ca10">


https://github.com/user-attachments/assets/2aba2a4e-c555-4a73-b5a7-32b9d8f372c0




Features

- > Authorization and authentication with JWT (JSON Web Token)
- > Protected Endpoints
- > Email Validation
- > Use of Hashed passwords
- > Jenkins Job that builds the docker image when a GitHub commit happens on the main branch

Technologies used

- > FastAPI
- > Maria DB
- > SqlAlchemy
- > Docker

use app from docker

```sh
docker-compose up --build
```

use app on local env

```sh
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

run tests

```sh
pytest -s tests
```
