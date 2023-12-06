from app.database import SessionLocal
from app.settings import settings
from elasticsearch import Elasticsearch

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_es():
    es = Elasticsearch(settings.ELASTICSEARCH_HOSTS)
    try:
        yield es
    finally:
        es.close()
