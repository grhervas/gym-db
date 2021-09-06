from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import (Program, Block, Workout,
                    Workout_set, Exercise, Muscle,
                    Log_workout, Log_set, Historic_pr)


def main():
    """Main entry point of the program"""

    # Connect to the database using SQLAlchemy
    # sqlite_filepath = Path("./../gym_database.db").resolve()
    engine = create_engine(f"sqlite:///data/db/gym_database.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Block).all()
    for row in query:
        print(row)


if __name__ == "__main__":
    main()
