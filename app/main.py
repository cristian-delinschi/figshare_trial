from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/register/", response_model=schemas.AccountRegister)
def register(account: schemas.AccountRegister, db: Session = Depends(get_db)):
    db_account = crud.get_account_by_email(db, email=account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_account(db=db, account=account)


@app.get("/accounts/", response_model=list[schemas.AccountResponse])
def get_accounts(db: Session = Depends(get_db)):
    return crud.get_accounts(db)


@app.get("/accounts/{id}/", response_model=schemas.AccountResponse)
def get_account(acc_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_account_by_id(db, acc_id=acc_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@app.put("/accounts/{account_id}", response_model=schemas.AccountUpdate)
def update_account(acc_id: int, account: schemas.AccountUpdate, db: Session = Depends(get_db)):
    email_check = crud.get_account_by_email(db, email=account.email)
    if email_check:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_account = crud.update_account(db=db, acc_id=acc_id, account_update=account)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    return db_account


@app.delete("/accounts/{id}", response_model=schemas.AccountResponse)
def delete_account(acc_id: int, db: Session = Depends(get_db)):
    db_account = crud.delete_account(db=db, acc_id=acc_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account
