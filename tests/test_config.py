import asyncio
import os
from os import path
from typing import List

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database.schema import Users
from app.main import create_app
from app.database.conn import db, Base
from app.models import UserToken
from app.routes.auth import create_access_token


@pytest.fixture(scope="session")
def app():
    os.environ["API_ENV"] = "test"
    return create_app()


@pytest.fixture(scope="session")
def client(app):
    Base.metadata.create_all(db.engine)
    return TestClient(app=app)


@pytest.fixture(scope="function", autouse=True)
def session():
    sess = next(db.session())
    yield sess
    clear_all_table_data(
        session=sess,
        metadata=Base.metadata,
        except_tables=[]
    )
    sess.rollback()


@pytest.fixture(scope="function")
def login(session):
    """
    로그인 테스트
    """
    db_user = Users.create(session=session, email="ryan_test@dingrr.com", pw="123")
    session.commit()
    access_token = create_access_token(data=UserToken.from_orm(db_user).dict(exclude={'pw', 'marketing_agree'}),)
    return dict(Authorization=f"Bearer {access_token}")


def clear_all_table_data(session: Session, metadata, except_tables: List[str] = None):
    session.execute("SET FOREIGN_KEY_CHECKS = 0;")
    for table in metadata.sorted_tables:
        if table.name not in except_tables:
            session.execute(table.delete())
    session.execute("SET FOREIGN_KEY_CHECKS = 1;")
    session.commit()
