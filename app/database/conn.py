from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import query, sessionmaker
from dive3m.utils.logger import Logger


def _database_exist(engine, schema_name):
    query = f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{schema_name}'"
    with engine.connect() as conn:
        result_proxy = conn.execute(query)
        result = result_proxy.scalar()
        return bool(result)


def _drop_database(engine, schema_name):
    with engine.connect() as conn:
        conn.execute(f"DROP DATABASE {schema_name};")


def _create_database(engine, schema_name):
    with engine.connect() as conn:
        conn.execute(f"CREATE DATABASE {schema_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;")


class SQLAlchemy:
    def __init__(self, app: FastAPI = None, **kwargs):
        self._engine = None
        self._session = None
        if app is not None:
            self.init_app(app=app, **kwargs)

    def init_app(self, app: FastAPI, **kwargs):
        """
        DB 초기화 함수
        :param app: FastAPI app
        :param kwargs:
        :return:
        """
        database_url = kwargs.get("DB_URL")
        pool_recycle = kwargs.setdefault("DB_POOL_RECYCLE", 900)
        echo = kwargs.setdefault("DB_ECHO", True)
        is_testing = kwargs.setdefault("TEST_MODE", False)

        self._engine = create_engine(
            database_url,
            echo=echo,
            pool_recycle=pool_recycle,
            pool_pre_ping=True,
        )
        db_url = self._engine.url
        self._table_name = str(db_url).split(f"{db_url.port}")[1].split('?')[0].split('/')[1]
        schema_name = db_url.database
        if not _database_exist(self._engine, schema_name):
            _create_database(self._engine, schema_name)
        if is_testing:
            db_url = self._engine.url
            if db_url.host != "localhost":
                raise Exception("db host must be 'localhost' in test environment")
            except_schema_db_url = f"{db_url.drivername}://{db_url.username}@{db_url.host}"
            schema_name = db_url.database
            temp_engine = create_engine(
                except_schema_db_url,
                echo=echo,
                pool_recycle=pool_recycle,
                pool_pre_ping=True
            )
            if _database_exist(temp_engine, schema_name):
                _drop_database(temp_engine, schema_name)
            _create_database(temp_engine, schema_name)
            temp_engine.dispose()
        self._session = sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )

        @app.on_event("startup")
        def startup():
            self._engine.connect()
            Logger.info("DB connected.")

        @app.on_event("shutdown")
        def shutdown():
            self._session.close_all()
            self._engine.dispose()
            Logger.info("DB disconnected")

    def get_db(self):
        """
        요청마다 db세션 유지하는 함수
        :return:
        """
        if self._session is None:
            raise Exception("must be called 'init_app'")
        db_session = None
        try:
            db_session = self._session()
            yield db_session
        finally:
            db_session.close()

    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self._engine

    @property
    def table_exist(self):
        q = f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{self._table_name}'"
        with self._engine.connect() as conn:
            result_proxy = conn.execute(q)
            result = result_proxy.scalar()
            return bool(result)


db = SQLAlchemy()
Base = declarative_base()
