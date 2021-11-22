"""
This is the gym module and supports all the ReST actions for the
GYM collection
"""

# from datetime import datetime
from models import Program, ProgramSchema
from config import db
from flask import make_response, abort


def read_all_programs():
    """
    This function responds to a GET request for /api/programs
    with the complete list of programs

    :return:    json string of list of programs sorted by start
                date
    """
    # Create list of programs from db query
    programs = Program.query.order_by(Program.date_start).all()

    # Serialize the data for the response
    program_schema = ProgramSchema(many=True)
    data = program_schema.dump(programs)

    return data


def create_program(program):
    """
    This function creates a new program in the Program structure
    based on the passed in program data

    :param program:     program to create
    :return:            201 on sucess, 406 on program exists
    """
    program_desc = program.get("program_desc")
    date_start = program.get("date_start")

    existing_program = (
        Program.query.filter(Program.program_desc == program_desc,
                             Program.date_start == date_start)
               .one_or_none()
    )

    existing_start_dates = [r.date_start for r in Program.query]

    # Can we insert new program?
    if existing_program is None and date_start not in existing_start_dates:

        # Create a program instance using the schema and the passed in program
        program_schema = ProgramSchema()
        new_program = program_schema.load(program, session=db.session)

        # Add the program to the database
        db.session.add(new_program)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = program_schema.dump(new_program)

        return data, 201

    # Otherwise, program already exists
    else:
        abort(
            409,
            f"Program {program_desc} started on {date_start} already exists!"
        )
