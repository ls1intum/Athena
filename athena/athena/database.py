import importlib
import os
from contextlib import contextmanager

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///../data/data.sqlite")
Base = declarative_base()

# SQLite specific configuration
is_sqlite = SQLALCHEMY_DATABASE_URL.startswith("sqlite:///")
if is_sqlite:
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables(exercise_type: str):
    """
    Create all tables for models in athena.models, whose name starts with "DB"+exercise_type.name.title().
    Also create all tables which have been registered previously using `create_additional_table_if_not_exists`.
    """
    model_module = importlib.import_module("athena.models")
    model_class_name_start = "DB" + exercise_type.title()
    for model_class_name in dir(model_module):
        if model_class_name.startswith(model_class_name_start):
            # Get the model class so that Base knows about it
            getattr(model_module, model_class_name)
    Base.metadata.create_all(engine)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
