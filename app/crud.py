from sqlalchemy.orm import Session

from . import auth, models, schemas


def create_account(db: Session, account: schemas.AccountRegister):
    hashed_password = auth.get_password_hash(account.password)
    db_account = models.Account(
        name=account.name,
        email=account.email,
        password=account.password,
        hashed_password=hashed_password
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def get_accounts(db: Session):
    return db.query(models.Account).all()


def get_account_by_id(db: Session, acc_id: int):
    return db.query(models.Account).filter(models.Account.id == acc_id).first()


def get_account_by_email(db: Session, email: str):
    return db.query(models.Account).filter(models.Account.email == email).first()


def update_account(db: Session, acc_id: int, account_update: schemas.AccountUpdate):
    db_account = db.query(models.Account).filter(models.Account.id == acc_id).first()
    if db_account:
        acc = account_update.dict(exclude_unset=True)
        del acc['id']
        for key, value in acc.items():
            setattr(db_account, key, value)
        db.commit()
        db.refresh(db_account)
    return db_account


def delete_account(db: Session, acc_id: int):
    db_account = db.query(models.Account).filter(models.Account.id == acc_id).first()
    if db_account:
        db.delete(db_account)
        db.commit()
    return db_account
