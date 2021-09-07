CREATE TABLE program ( 
    program_id INTEGER NOT NULL PRIMARY KEY,
    program_desc VARCHAR,
    date_start DATE,
    date_end DATE,
    objective VARCHAR,
    CHECK (date_start < date_end 
           OR
           (date_start IS NULL OR date_end IS NULL))
);

CREATE TABLE block (
    block_id INTEGER NOT NULL PRIMARY KEY,
    block_desc VARCHAR,
    program_id INTEGER NOT NULL REFERENCES program
);

CREATE TABLE workout (
    workout_id INTEGER NOT NULL PRIMARY KEY,
    workout_desc VARCHAR,
    block_id INTEGER NOT NULL REFERENCES block,
    date_workout DATE,
    week INTEGER CHECK (week > 0),
    day INTEGER CHECK (day > 0),
    UNIQUE(block_id, week, day) ON CONFLICT ABORT,
    UNIQUE(block_id, date_workout) ON CONFLICT ABORT
);

CREATE TABLE exercise (
    exercise_id INTEGER NOT NULL PRIMARY KEY,
    exercise_desc VARCHAR NOT NULL
);

CREATE TABLE workout_set (
    workout_set_id INTEGER NOT NULL PRIMARY KEY,
    workout_id INTEGER NOT NULL REFERENCES workout,
    exercise_id INTEGER NOT NULL REFERENCES exercise,
    set_id INTEGER NOT NULL CHECK (set_id > 0),
    no_reps INTEGER CHECK (no_reps > 0),
    perc_rm REAL CHECK (0 < perc_rm AND perc_rm <= 100),
    min_rpe INTEGER CHECK (0 <= min_rpe AND min_rpe <= 10),
    max_rpe INTEGER CHECK (0 <= max_rpe AND max_rpe <= 10),
    rest_min REAL CHECK (rest_min >= 0),
    UNIQUE(workout_id, exercise_id, set_id) ON CONFLICT ABORT,
    CHECK ( min_rpe <= max_rpe 
            OR
            (min_rpe IS NULL OR max_rpe IS NULL) )
);

CREATE TABLE log_workout (
    log_workout_id INTEGER NOT NULL PRIMARY KEY,
    workout_id INTEGER UNIQUE NOT NULL REFERENCES workout,
    date_workout_done DATE,
    duration_min REAL CHECK (duration_min > 0),
    intensity REAL CHECK (0 <= intensity AND intensity <= 10),
    comment_workout VARCHAR,
    date_reg DATE NOT NULL DEFAULT (DATE('now')),
    CHECK ( date_workout_done <= date_reg )
);

CREATE TABLE log_set (
    log_set_id INTEGER NOT NULL PRIMARY KEY,
    workout_set_id INTEGER UNIQUE NOT NULL REFERENCES workout_set,
    log_workout_id INTEGER NOT NULL REFERENCES log_workout,
    no_reps_done INTEGER CHECK (no_reps_done >= 0),
    weight_done REAL CHECK (weight_done > 0),
    rpe_done INTEGER CHECK (0 <= rpe_done AND rpe_done <= 10),
    comment_set VARCHAR
);

CREATE TABLE historic_pr (
    pr_id INTEGER NOT NULL PRIMARY KEY,
    date_pr DATE,
    exercise_id INTEGER NOT NULL REFERENCES exercise,
    no_reps_pr INTEGER NOT NULL CHECK (no_reps_pr > 0),
    weight_pr REAL NOT NULL CHECK (weight_pr > 0),
    date_reg DATE NOT NULL DEFAULT (DATE('now')),
    CHECK ( date_pr <= date_reg )
);

CREATE TABLE muscle (
    muscle_id INTEGER NOT NULL PRIMARY KEY,
    muscle_desc VARCHAR NOT NULL
);

CREATE TABLE exercise_muscle (
    exercise_muscle_id INTEGER NOT NULL PRIMARY KEY,
    exercise_id INTEGER NOT NULL REFERENCES exercise,
    muscle_id INTEGER NOT NULL REFERENCES muscle
);
