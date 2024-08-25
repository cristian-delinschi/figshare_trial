from sqlalchemy.orm import Session
from validate_email_address import validate_email
from datetime import datetime

from . import auth, models, schemas


def create_account(db: Session, account: schemas.AccountRegister):
    hashed_password = auth.get_password_hash(account.password)
    db_account = models.Account(
        name=account.name,
        email=account.email,
        is_active=True,
        password=account.password,
        hashed_password=hashed_password,
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    set_last_login_date(db, email=account.email)
    db.commit()
    db.refresh(db_account)
    return db_account


def get_accounts(db: Session):
    return db.query(models.Account).all()


def get_account_by_id(db: Session, acc_id: int):
    return db.query(models.Account).filter(models.Account.id == acc_id).first()


def get_account_by_email(db: Session, email: str):
    return db.query(models.Account).filter(models.Account.email == email).first()


def update_account(db: Session, email: str, account_update: schemas.AccountUpdate):
    db_account = db.query(models.Account).filter(models.Account.email == email).first()
    if db_account:
        acc = account_update.dict(exclude_unset=True)
        for key, value in acc.items():
            setattr(db_account, key, value)
        db.commit()
        db.refresh(db_account)
    return db_account


def delete_account(db: Session, email: str):
    db_account = db.query(models.Account).filter(models.Account.email == email).first()
    if db_account:
        db.delete(db_account)
        db.commit()
    return db_account


def set_last_login_date(db: Session, email: str):
    db_account = db.query(models.Account).filter(models.Account.email == email).first()
    setattr(db_account, 'last_login_date', datetime.now())
    db.commit()
    db.refresh(db_account)
    return db_account


def check_email(email):
    is_valid = validate_email(email, verify=False)
    return is_valid
