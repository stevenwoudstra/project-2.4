from sqlalchemy import create_engine
from sqlalchemy.orm import Query, scoped_session, sessionmaker

__all__ = ["Query", "create_engine_and_session"]

from database.db_model import DBModel

def create_engine_and_session(app):
    app.engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

    app.session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=True,
            binds={DBModel: app.engine},
        )
    )