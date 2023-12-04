from app.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if settings.SQLALCHEMY_DATABASE_URI is None:
    raise ValueError(
        "SQLALCHEMY_DATABASE_URI should be setting. Check your .env file",
    )

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI.unicode_string(),
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
