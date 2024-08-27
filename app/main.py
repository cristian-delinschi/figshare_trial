from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm

from .database import engine, get_db
from . import crud, models, schemas, auth
from .git_auth import router as auth_app

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_app)


@app.post("/token", response_model=schemas.LoginResponse)
async def authorization(
        form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    account = crud.get_account_by_email(db, email=form_data.username)
    if not account or not auth.verify_password(form_data.password, account.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )

    crud.set_last_login_date(db, email=form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register/", response_model=schemas.AccountResponse)
def register(
        name: str = Form(..., description="insert new account name"),
        email: str = Form(..., description="insert new account email"),
        password: str = Form(..., description="insert new account password"),
        db: Session = Depends(get_db)
):
    db_account = crud.get_account_by_email(db, email=email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")

    if not crud.check_email(email):
        raise HTTPException(status_code=400, detail="Email is not valid")

    account = schemas.AccountRegister(name=name, email=email, password=password)
    return crud.create_account(db=db, account=account)


@app.get("/accounts/", response_model=list[schemas.AccountResponse])
def get_accounts(
        db: Session = Depends(get_db),
        current_account: dict = Depends(auth.get_current_account)
):
    return crud.get_accounts(db)


@app.get("/account/{id}/", response_model=schemas.AccountResponse)
def get_account(
        acc_id: int, db: Session = Depends(get_db),
        current_account: dict = Depends(auth.get_current_account)
):
    db_account = crud.get_account_by_id(db, acc_id=acc_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@app.patch("/account_partial_update", response_model=schemas.AccountResponse)
def update_partial_account(
        email: str = Form(..., description="Account email which account should be updated"),
        name: str = Form(None),
        password: str = Form(None),
        is_active: bool = Form(None),
        db: Session = Depends(get_db),
        current_account: dict = Depends(auth.get_current_account)
):
    if not crud.check_email(email):
        raise HTTPException(status_code=400, detail="Email is not valid")

    account_update = schemas.AccountPartialUpdate(name=name, email=email, password=password, is_active=is_active)
    db_account = crud.update_account(db=db, email=email, account_update=account_update)

    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    return db_account


@app.put("/account_full_update", response_model=schemas.AccountResponse)
def update_full_account(
        email: str = Form(..., description="Account email which account should be updated"),
        name: str = Form(...),
        password: str = Form(...),
        is_active: bool = Form(...),
        db: Session = Depends(get_db),
        current_account: dict = Depends(auth.get_current_account)
):
    if not crud.check_email(email):
        raise HTTPException(status_code=400, detail="Email is not valid")

    account_update = schemas.AccountFullUpdate(name=name, email=email, password=password, is_active=is_active)
    db_account = crud.update_account(db=db, email=email, account_update=account_update)

    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    return db_account


@app.delete("/account_delete", response_model=schemas.AccountResponse)
def delete_account(
        email: str = Form(..., description="Account email which account should be deleted"),
        db: Session = Depends(get_db),
        current_account: dict = Depends(auth.get_current_account)
):
    db_account = crud.delete_account(db=db, email=email)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account
