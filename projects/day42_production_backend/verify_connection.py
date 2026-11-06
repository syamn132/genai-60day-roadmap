
from sqlalchemy import text

from app.db.session import engine


def main():

    print("DAY 42 — DATABASE CONNECTION TEST")

    with engine.connect() as connection:

        result = connection.execute(
            text(
                "SELECT current_database(), current_user"
            )
        )

        database_name, database_user = result.one()

        print("Database:", database_name)
        print("Connected user:", database_user)
        print("Connection status: SUCCESS")


if __name__ == "__main__":
    try:
        main()
    finally:
        engine.dispose()
