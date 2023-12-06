import argparse

from app.database import engine
from sqlalchemy import text


parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, required=True)


def init_db(path: str):
    with engine.connect() as con:
        with open(path) as file:
            query = text(file.read())
            con.execute(query)


if __name__ == "__main__":
    args = parser.parse_args()
    init_db(args.path)
