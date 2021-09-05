from sqlalchemy import (Column, Integer, Float, Date, String,
                        ForeignKey, Table, UniqueConstraint, CheckConstraint)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# Association table for M-M relationship Exercises-Muscles using
# class Table()
exercise_muscle = Table(
    "exercise_muscle",
    Base.metadata,
    Column("exercise_muscle_id", Integer, primary_key=True),
    Column("exercise_id", Integer, ForeignKey("exercise.exercise_id")),
    Column("muscle_id", Integer, ForeignKey("muscle.muscle_id"))
)


class Program(Base):
    __tablename__ = "program"
    __table_args__ = (
        CheckConstraint("""date_start < date_end
                           OR
                           (date_start IS NULL OR date_end IS NULL)""")
    )

    program_id = Column(Integer, primary_key=True)
    program_desc = Column(String)
    date_start = Column(Date)
    date_end = Column(Date)
    objective = Column(String)

    blocks = relationship("Block", back_populates="program")

    def __repr__(self):
        return f"""<Program(id={self.program_id},
                            desc={self.program_desc},
                            date_start={self.date_start},
                            date_end={self.date_end},
                            objective={self.objective})>"""


class Block(Base):
    __tablename__ = "block"

    block_id = Column(Integer, primary_key=True)
    block_desc = Column(String)
    program_id = Column(Integer, ForeignKey("program.program_id"),
                        nullable=False)

    program = relationship("Program", back_populates="blocks")
    workouts = relationship("Workout", back_populates="block")

    def __repr__(self):
        return f"""<Block(id={self.block_id},
                          desc={self.block_desc},
                          program={self.program.program_desc})>"""


class Workout(Base):
    __tablename__ = "workout"

    workout_id = Column(Integer, primary_key=True)
    block_id = Column(Integer, ForeignKey("block.block_id"),
                      nullable=False)
    week = Column(Integer, CheckConstraint("week > 0"))
    day = Column(Integer, CheckConstraint("day > 0"))

    block = relationship("Block", back_populates="workouts")
    workout_sets = relationship("Workout_set", back_populates="workout")
    log_workout = relationship("Log_workout", back_populates="workout",
                               uselist=False)

    def __repr__(self):
        return f"""<Workout(id={self.workout_id},
                            program={self.block.program.program_desc},
                            block={self.block.block_desc},
                            week={self.week},
                            day={self.day})>"""


class Exercise(Base):
    __tablename__ = "exercise"

    exercise_id = Column(Integer, primary_key=True)
    exercise_desc = Column(String, nullable=False)

    historic_prs = relationship("Historic_pr", back_populates="exercise")
    workout_sets = relationship("Workout_set", back_populates="exercise")
    # This is defined for the case of using Table() class
    # as association table for Exercises-Muscles
    muscles = relationship("Muscle", secondary=exercise_muscle,
                           back_populates="exercises")
    # # If using Association Object
    # muscles = relationship("Exercise_muscle", back_populates="exercise")

    def __repr__(self):
        return f"""<Exercise(id={self.exercise_id},
                             desc={self.exercise_desc})>"""


# # Many-to-many association Exercises-Muscles via Association Object
# class Exercise_muscle(Base):
#     __tablename__ = "exercise_muscle"

#     exercise_muscle_id = Column(Integer, primary_key=True)
#     exercise_id = Column(Integer, ForeignKey("exercise.exercise_id"),
#                          nullable=False)
#     muscle_id = Column(Integer, ForeignKey("muscle.muscle_id"),
#                        nullable=False)

#     muscle = relationship("Muscle", back_populates="exercises")
#     exercise = relationship("Exercise", back_populates="muscles")


class Muscle(Base):
    __tablename__ = "muscle"

    muscle_id = Column(Integer, primary_key=True)
    muscle_desc = Column(String, nullable=False)
    # This is defined for the case of using Table() class
    # as association table for Exercises-Muscles
    exercises = relationship("Exercise", secondary=exercise_muscle,
                             back_populates="muscles")
    # # If using Association Object ()
    # exercises = relationship("Exercise_muscle", back_populates="muscle")

    def __repr__(self):
        return f"""<Muscle(id={self.muscle_id},
                           desc={self.muscle_desc})>"""


class Workout_set(Base):
    __tablename__ = "workout_set"
    __table_args__ = (
        UniqueConstraint("workout_id", "exercise_id", "set_id"),
        CheckConstraint("""min_rpe <= max_rpe
                           OR
                           (min_rpe IS NULL OR max_rpe IS NULL)""")
    )

    workout_set_id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey("workout.workout_id"),
                        nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercise.exercise_id"),
                         nullable=False)
    set_id = Column(Integer, CheckConstraint("set_id > 0"),
                    nullable=False)
    no_reps = Column(Integer, CheckConstraint("no_reps > 0"))
    perc_rm = Column(Float, CheckConstraint("0 < perc_rm AND perc_rm <= 100"))
    min_rpe = Column(Integer,
                     CheckConstraint("0 <= min_rpe AND min_rpe <= 10"))
    max_rpe = Column(Integer,
                     CheckConstraint("0 <= max_rpe AND max_rpe <= 10"))

    log_set = relationship("Log_set", back_populates="workout_set",
                           uselist=False)
    workout = relationship("Workout", back_populates="workout_sets")
    exercise = relationship("Exercise", back_populates="workout_sets")

    def __repr__(self):
        return f"""<Workout_set(id={self.workout_set_id},
                                program={self.workout.block.program.program_desc},
                                block={self.workout.block.block_desc},
                                week={self.workout.week},
                                day={self.workout.day}),
                                exercise={self.exercise.exercise_desce},
                                set_id={self.set_id}>"""


class Log_workout(Base):
    __tablename__ = "log_workout"
    __table_args__ = (
        CheckConstraint("date_workout <= date_reg")
    )

    log_workout_id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey("workout.workout_id"),
                        unique=True, nullable=False)
    date_workout = Column(Date)
    duration_min = Column(Float, CheckConstraint("duration_min > 0"))
    intensity = Column(Float,
                       CheckConstraint("0 <= intensity AND intensity <= 10"))
    comment_workout = Column(String)
    date_reg = Column(Date, nullable=False)

    log_sets = relationship("Log_set", back_populates="log_workout")
    workout = relationship("Workout", back_populates="log_workout")

    def __repr__(self):
        return f"""<Log_workout(id={self.log_workout_id},
                                date={self.date_workout},
                                program={self.workout.block.program.program_desc},
                                block={self.workout.block.block_desc},
                                week={self.workout.week},
                                day={self.workout.day})>"""


class Log_set(Base):
    __tablename__ = "log_set"

    log_set_id = Column(Integer, primary_key=True)
    workout_set_id = Column(Integer, ForeignKey("workout_set.workout_set_id"),
                            unique=True, nullable=False)
    log_workout_id = Column(Integer, ForeignKey("log_workout.log_workout_id"),
                            nullable=False)
    no_reps_done = Column(Integer, CheckConstraint("no_reps_done >= 0"))
    weight_done = Column(Float, CheckConstraint("weight_done > 0"))
    rpe_done = Column(Integer,
                      CheckConstraint("0 <= rpe_done AND rpe_done <= 10"))
    comment_set = Column(String)

    log_workout = relationship("Log_workout", back_populates="log_sets")
    workout_set = relationship("Workout_set", back_populates="log_set")

    def __repr__(self):
        return f"""<Log_set(id={self.log_set_id},
                            date={self.log_workout.date_workout},
                            program={self.log_workout.workout.block.program.program_desc},
                            block={self.log_workout.workout.block.block_desc},
                            week={self.log_workout.workout.week},
                            day={self.log_workout.workout.day},
                            exercise={self.workout_set.exercise.exercise_desc},
                            set_id={self.workout_set.set_id})>"""


class Historic_pr(Base):
    __tablename__ = "historic_pr"
    __table_args__ = (
        CheckConstraint("date_pr <= date_reg")
    )

    pr_id = Column(Integer, primary_key=True)
    date_pr = Column(Date)
    exercise_id = Column(Integer, ForeignKey("exercise.exercise_id"),
                         nullable=False)
    no_reps_pr = Column(Integer, CheckConstraint("no_reps_pr > 0"),
                        nullable=False)
    weight_pr = Column(Float, CheckConstraint("weight_pr > 0"),
                       nullable=False)
    date_reg = Column(Date, nullable=False)

    exercise = relationship("Exercise", back_populates="historic_prs")

    def __repr__(self):
        return f"""<Historic_pr(id={self.pr_id},
                                exercise={self.exercise.exercise_desc},
                                date={self.date_pr},
                                no_reps={self.no_reps_pr},
                                weight={self.weight_pr})>"""