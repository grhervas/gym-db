from config import db, ma
from datetime import datetime
# from sqlalchemy import (Column, Integer, Float, Date, String,
#                         ForeignKey, Table, UniqueConstraint, CheckConstraint)
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.sql.functions import current_timestamp, now


# Base = declarative_base()

# Association table for M-M relationship Exercises-Muscles using
# class Table()
exercise_muscle = db.Table(
    "exercise_muscle",
    # db.metadata,
    # Base.metadata,
    # db.Column("exercise_muscle_id", db.Integer, primary_key=True),
    db.Column("exercise_id", db.Integer, db.ForeignKey("exercise.exercise_id")),
    db.Column("muscle_id", db.Integer, db.ForeignKey("muscle.muscle_id"))
)


# Do SQLAlchemy Table objects need and SQLAlchemyAutoSchema class equivalent??


class Program(db.Model):
    __tablename__ = "program"
    __table_args__ = (
        db.CheckConstraint("""
                           date_start < date_end
                           OR
                           (date_start IS NULL OR date_end IS NULL)
                           """),
    )

    program_id = db.Column(db.Integer, primary_key=True)
    program_desc = db.Column(db.String)
    date_start = db.Column(db.Date)
    date_end = db.Column(db.Date)
    objective = db.Column(db.String)

    blocks = db.relationship("Block", cascade="all, delete-orphan", back_populates="program")

    def __repr__(self):
        return (f"<Program(id={self.program_id}," +
                f"desc={self.program_desc}," +
                f"date_start={self.date_start}," +
                f"date_end={self.date_end}," +
                f"objective={self.objective})>")


class Block(db.Model):
    __tablename__ = "block"

    block_id = db.Column(db.Integer, primary_key=True)
    block_desc = db.Column(db.String)
    program_id = db.Column(db.Integer, db.ForeignKey("program.program_id"),
                           nullable=False)

    program = db.relationship("Program", back_populates="blocks")
    workouts = db.relationship("Workout", cascade="all, delete-orphan", back_populates="block")

    def __repr__(self):
        return (f"<Block(id={self.block_id}," +
                f"desc={self.block_desc}," +
                f"program={self.program.program_desc})>")


class Workout(db.Model):
    __tablename__ = "workout"
    __table_args__ = (
        db.UniqueConstraint("block_id", "week", "day"),
        db.UniqueConstraint("block_id", "date_workout")
    )

    workout_id = db.Column(db.Integer, primary_key=True)
    workout_desc = db.Column(db.String)
    block_id = db.Column(db.Integer, db.ForeignKey("block.block_id"),
                         nullable=False)
    date_workout = db.Column(db.Date)
    week = db.Column(db.Integer, db.CheckConstraint("week > 0"))
    day = db.Column(db.Integer, db.CheckConstraint("day > 0"))

    block = db.relationship("Block", back_populates="workouts")
    workout_sets = db.relationship("WorkoutSet", cascade="all, delete-orphan", back_populates="workout")
    log_workout = db.relationship("LogWorkout", cascade="all, delete-orphan", back_populates="workout",
                                  uselist=False)

    def __repr__(self):
        return (f"<Workout(id={self.workout_id}," +
                f"name={self.workout_desc}," +
                f"program={self.block.program.program_desc}," +
                f"block={self.block.block_desc}," +
                f"date={self.date_workout}," +
                f"week={self.week}," +
                f"day={self.day})>")


class Exercise(db.Model):
    __tablename__ = "exercise"

    exercise_id = db.Column(db.Integer, primary_key=True)
    exercise_desc = db.Column(db.String, nullable=False)

    historic_prs = db.relationship("HistoricPR", back_populates="exercise")
    workout_sets = db.relationship("WorkoutSet", back_populates="exercise")
    # This is defined for the case of using Table() class
    # as association table for Exercises-Muscles
    muscles = db.relationship("Muscle", secondary=exercise_muscle,
                              cascade="all, delete", back_populates="exercises")
    # # If using Association Object
    # muscles = relationship("Exercise_muscle", back_populates="exercise")

    def __repr__(self):
        return (f"<Exercise(id={self.exercise_id}," +
                f"desc={self.exercise_desc})>")


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


class Muscle(db.Model):
    __tablename__ = "muscle"

    muscle_id = db.Column(db.Integer, primary_key=True)
    muscle_desc = db.Column(db.String, nullable=False)
    # This is defined for the case of using Table() class
    # as association table for Exercises-Muscles
    exercises = db.relationship("Exercise", secondary=exercise_muscle,
                                cascade="all, delete", back_populates="muscles")
    # # If using Association Object ()
    # exercises = relationship("Exercise_muscle", back_populates="muscle")

    def __repr__(self):
        return (f"<Muscle(id={self.muscle_id}," +
                f"desc={self.muscle_desc})>")


class WorkoutSet(db.Model):
    __tablename__ = "workout_set"
    __table_args__ = (
        # UniqueConstraint("workout_id", "exercise_id", "set_id"),
        db.CheckConstraint("""min_rpe <= max_rpe
                           OR
                           (min_rpe IS NULL OR max_rpe IS NULL)"""),
    )

    workout_set_id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workout.workout_id"),
                           nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.exercise_id"),
                            nullable=False)
    set_id = db.Column(db.Integer, db.CheckConstraint("set_id > 0"),
                       nullable=False)
    no_reps = db.Column(db.Integer, db.CheckConstraint("no_reps >= 0"))
    weight = db.Column(db.Float, db.CheckConstraint("weight >= 0"))
    perc_rm = db.Column(db.Float, db.CheckConstraint("0 < perc_rm AND perc_rm <= 100"))
    min_rpe = db.Column(db.Integer,
                        db.CheckConstraint("0 <= min_rpe AND min_rpe <= 10"))
    max_rpe = db.Column(db.Integer,
                        db.CheckConstraint("0 <= max_rpe AND max_rpe <= 10"))
    rest_min = db.Column(db.Float, db.CheckConstraint("rest_min >= 0"))

    log_set = db.relationship("LogSet", cascade="all, delete-orphan", back_populates="workout_set",
                              uselist=False)
    workout = db.relationship("Workout", back_populates="workout_sets")
    exercise = db.relationship("Exercise", back_populates="workout_sets")

    def __repr__(self):
        return (f"<WorkoutSet(id={self.workout_set_id}," +
                f"program={self.workout.block.program.program_desc}," +
                f"block={self.workout.block.block_desc}," +
                f"date={self.workout.date_workout}," +
                f"week={self.workout.week}," +
                f"day={self.workout.day}," +
                f"exercise={self.exercise.exercise_desc}," +
                f"set_id={self.set_id})>")


class LogWorkout(db.Model):
    __tablename__ = "log_workout"
    __table_args__ = (
        db.CheckConstraint("date_workout_done <= date_reg"),
    )

    log_workout_id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workout.workout_id"),
                           unique=True, nullable=False)
    date_workout_done = db.Column(db.Date)
    duration_min = db.Column(db.Float, db.CheckConstraint("duration_min > 0"))
    intensity = db.Column(db.Float,
                          db.CheckConstraint("0 <= intensity AND intensity <= 10"))
    comment_workout = db.Column(db.String)
    date_reg = db.Column(db.Date, nullable=False,
                         default=datetime.utcnow, onupdate=datetime.utcnow)

    log_sets = db.relationship("LogSet", cascade="all, delete-orphan", back_populates="log_workout")
    workout = db.relationship("Workout", back_populates="log_workout")

    def __repr__(self):
        return (f"<Log_workout(id={self.log_workout_id}," +
                f"date={self.date_workout_done}," +
                f"program={self.workout.block.program.program_desc}," +
                f"block={self.workout.block.block_desc}," +
                f"week={self.workout.week}," +
                f"day={self.workout.day})>")


class LogSet(db.Model):
    __tablename__ = "log_set"

    log_set_id = db.Column(db.Integer, primary_key=True)
    workout_set_id = db.Column(db.Integer, db.ForeignKey("workout_set.workout_set_id"),
                               unique=True, nullable=False)
    log_workout_id = db.Column(db.Integer, db.ForeignKey("log_workout.log_workout_id"),
                               nullable=False)
    no_reps_done = db.Column(db.Integer, db.CheckConstraint("no_reps_done >= 0"))
    weight_done = db.Column(db.Float, db.CheckConstraint("weight_done >= 0"))
    rpe_done = db.Column(db.Integer,
                         db.CheckConstraint("0 <= rpe_done AND rpe_done <= 10"))
    comment_set = db.Column(db.String)

    log_workout = db.relationship("LogWorkout", back_populates="log_sets")
    workout_set = db.relationship("WorkoutSet", back_populates="log_set")

    def __repr__(self):
        return (f"<LogSet(id={self.log_set_id}," +
                f"date={self.log_workout.date_workout_done}," +
                f"program={self.log_workout.workout.block.program.program_desc}," +
                f"block={self.log_workout.workout.block.block_desc}," +
                f"week={self.log_workout.workout.week}," +
                f"day={self.log_workout.workout.day}," +
                f"exercise={self.workout_set.exercise.exercise_desc}," +
                f"set_id={self.workout_set.set_id})>")


class HistoricPR(db.Model):
    __tablename__ = "historic_pr"
    __table_args__ = (
        db.CheckConstraint("date_pr <= date_reg"),
    )

    pr_id = db.Column(db.Integer, primary_key=True)
    date_pr = db.Column(db.Date)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.exercise_id"),
                            nullable=False)
    no_reps_pr = db.Column(db.Integer, db.CheckConstraint("no_reps_pr > 0"),
                           nullable=False)
    weight_pr = db.Column(db.Float, db.CheckConstraint("weight_pr > 0"),
                          nullable=False)
    date_reg = db.Column(db.Date, nullable=False,
                         default=datetime.utcnow, onupdate=datetime.utcnow)

    exercise = db.relationship("Exercise", back_populates="historic_prs")

    def __repr__(self):
        return (f"<HistoricPR(id={self.pr_id}," +
                f"exercise={self.exercise.exercise_desc}," +
                f"date={self.date_pr}," +
                f"no_reps={self.no_reps_pr}," +
                f"weight={self.weight_pr})>")


class ProgramSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Program
        # sqla_session = db.session
        load_instance = True


class BlockSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Block
        # sqla_session = db.session
        load_instance = True


class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        # sqla_session = db.session
        load_instance = True


class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        # sqla_session = db.session
        load_instance = True


class MuscleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Muscle
        # sqla_session = db.session
        load_instance = True


class WorkoutSetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutSet
        # sqla_session = db.session
        load_instance = True


class LogWorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LogWorkout
        # sqla_session = db.session
        load_instance = True


class LogSetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LogSet
        # sqla_session = db.session
        load_instance = True


class HistoricPRSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HistoricPR
        # sqla_session = db.session
        load_instance = True
