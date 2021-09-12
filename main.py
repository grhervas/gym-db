# from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import (Program, Block, Workout,
                    Workout_set, Exercise, Muscle,
                    Log_workout, Log_set, Historic_pr)

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re


def get_data_from_html(file):
    """
    Gets planning data from html file and returns dict with microcycle.

        Parameters:
            file (str or path): html file containing the info

        Returns:
            micro_dict (dict): dict containing same info organised
    """
    # "data/Micro0 Gonzalo septiembre2021.html"

    with open(file) as html_file:
        soup = BeautifulSoup(html_file, "html.parser")

        sessions_list = []
        sessions = soup.find_all("div", class_="dia")
        for session in sessions:
            session_dict = {}

            workout_desc = session.find("div", class_="titulo").text.lower()
            session_dict["workout_desc"] = workout_desc

            day = int(session.find("div", id="dia").text)
            month = int(session.find("div", id="mes").text)
            year = int(session.find("div", id="anyo").text)
            date = pd.Timestamp(day=day, month=month, year=year).date()
            session_dict["date_workout"] = date

            exercises_list = []
            exercises = (
                session.find("div", class_="cuerpo-boxdia")
                .find_all("div", re.compile("ejercicio.*"))
            )
            for exercise in exercises:
                exercise_dict = {}
                for element in exercise.find_all("div"):
                    exercise_dict[element.attrs['class'][0]] = element.text
                exercises_list.append(exercise_dict)
            session_dict["exercises"] = exercises_list

            sessions_list.append(session_dict)

        block_name = soup.find(id="microciclo").text
        micro_dict = {block_name: sessions_list}

    return micro_dict


def curate_exercises_data(exercises: list, col_names: list):
    """
    Apply some column transformations to make exercise data from workout
    ingestible by app.

        Parameters:
            exercises (list): list of exercises dicts
            col_names (list): list of standardized names to apply to dataframe

        Returns:
            df_exercises (pandas.DataFrame): dataframe containing workout exercises
                                             transformed
    """

    df_exercises = pd.DataFrame(exercises)
    # # Data quality criteria for workout session table
    # Standard names (only if matching length, else keep originals)
    if len(df_exercises.columns) == len(col_names):
        df_exercises.columns = col_names
    # Lowercase exercise names
    df_exercises.iloc[:, 0] = df_exercises.iloc[:, 0].str.lower()
    # Convert to numbers
    df_exercises.iloc[:, 1] = df_exercises.iloc[:, 1].str.extract(r"(\d+)").astype("int")
    df_exercises.iloc[:, 2] = df_exercises.iloc[:, 2].str.extract(r"(\d+)").astype("float")
    df_exercises.iloc[:, 3] = df_exercises.iloc[:, 3].str.extract(r"(\d+)").astype("float")
    df_exercises.iloc[:, 4] = df_exercises.iloc[:, 4].str.extract(r"(\d+)").astype("int")
    df_exercises.iloc[:, 5] = df_exercises.iloc[:, 5].str.extract(r"(\d+)").astype("int")
    df_exercises.iloc[:, 6] = df_exercises.iloc[:, 6].str.extract(r"(\d+)").astype("float")
    # In "Cargas (%)" and "Descanso (min)" change 0 --> NULL
    df_exercises.iloc[:, 2] = df_exercises.iloc[:, 2].replace(0.0, np.nan)
    df_exercises.iloc[:, 6] = df_exercises.iloc[:, 6].replace(0.0, np.nan)

    return df_exercises


def add_block(session, source_file=None, program: str = None):
    """
    Adds block of program from personal coach html file

        Parameters:
            session (SQLAlchemy.session object)
            source_file (str or path): the .html file that contains the info
            program (str): the gym program description name
    """

    COL_NAMES = ["Ejercicio", "Series", "Cargas (%)",
                 "Kilos", "Repeticiones", "RPE", "Descanso (min)"]

    # Check if program description already exists
    if program:
        program = (
            session.query(Program)
            .filter(Program.program_desc == program)
            .one_or_none()
        )
        program_id = program.program_id
    # If not (or not provided), create new generic program
    if program is None:
        program = Program()
        session.add(program)
        # If new, the program_id will be last element added
        program_id = session.query(Program).count()

    block_dict = get_data_from_html(source_file)

    for block_name, workouts_list in block_dict.items():
        # Check if block already exist (matching both name and program)
        block = (
            session.query(Block)
            .filter(Block.block_desc == block_name, Block.program_id == program_id)
            .one_or_none()
        )
        if block:
            block_id = block.block_id
        # If not, create it
        if block is None:
            block = Block(block_desc=block_name, program_id=program_id)
            session.add(block)
            # If new, the block_id will be last element added
            block_id = session.query(Block).count()

            # The loading of workouts and sets is only done if block doesn't exist
            # If block already exists we could branch an update function inside
            # (inside this add_block() or outside as a different call)
            for wod in workouts_list:
                workout = Workout(workout_desc=wod["workout_desc"],
                                  block_id=block_id,
                                  date_workout=wod["date_workout"])
                session.add(workout)
                workout_id = session.query(Workout).count()
                df_exercises = curate_exercises_data(wod["exercises"], COL_NAMES)

                # If exercise is not in Exercise lookup table, add it previously
                data_ex = df_exercises["Ejercicio"].unique()
                db_ex = [i[0] for i in session.query(Exercise.exercise_desc).all()]
                for new_exercise in list(set(data_ex) - set(db_ex)):
                    exercise = Exercise(exercise_desc=new_exercise)
                    session.add(exercise)

                # Then, insert row by row the results (exploding for as many series
                # per exercise there are)
                for index, row in df_exercises.iterrows():
                    for wod_set in range(row["Series"]):
                        set_id = wod_set + 1
                        workout_set = Workout_set(
                            workout_id=workout_id,
                            exercise_id=session.query(Exercise.exercise_id)
                                               .filter_by(exercise_desc=row["Ejercicio"])
                                               .scalar(),
                            set_id=set_id,
                            no_reps=row["Repeticiones"],
                            weight=row["Kilos"],
                            perc_rm=row["Cargas (%)"] if row["Cargas (%)"] != np.nan else None,
                            max_rpe=row["RPE"],
                            rest_min=row["Descanso (min)"] if row["Descanso (min)"] != np.nan else None
                        )
                        session.add(workout_set)

    session.commit()


def generate_program_excel():

    pass


def load_log_data():

    pass


def main():
    """Main entry point of the program"""

    # Connect to the database using SQLAlchemy
    # sqlite_filepath = Path("./../gym_database.db").resolve()
    engine = create_engine(f"sqlite:///data/db/gym_database.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    add_block(session, "data/Micro0 Gonzalo septiembre2021.html")

    query = session.query(Block).all()
    for row in query:
        print(row)


if __name__ == "__main__":
    main()
