INSERT INTO program (
    program_desc, 
    date_start,
    date_end,
    objective)
VALUES (
    "PHAT v2 (abr'21')",
    "2021-04-01",
    "2021-07-01",
    "Hypertrophy (+3kg)");

INSERT INTO block (
    block_desc,
    program_id )
VALUES (
    "Volume_1",
    1 );

INSERT INTO workout ( 
    workout_desc, block_id, date_workout, week, day )
VALUES (
    "Pierna", 1, "2021-04-09", 1, 3 );

INSERT INTO exercise (exercise_desc)
VALUES 
    ("press banca"),
    ("dominadas"),
    ("press militar"),
    ("sentadilla"),
    ("peso muerto"),
    ("peso muerto rumano"),
    ("hip thrust");

INSERT INTO muscle (muscle_desc)
VALUES 
    ("pectoral"),
    ("gemelo"),
    ("cuádriceps"),
    ("isquiotibiales"),
    ("glúteo"),
    ("bíceps"),
    ("tríceps"),
    ("antebrazo"),
    ("trapecio"),
    ("dorsal"),
    ("deltoide"),
    ("lumbar");

INSERT INTO workout_set (
    workout_id,
    exercise_id,
    set_id,
    no_reps,
    perc_rm,
    min_rpe,
    max_rpe )
VALUES ( 
    1,
    1,
    1,
    10,
    92.50,
    7,
    8 );

INSERT INTO log_workout(
    workout_id, date_workout, duration_min, intensity, comment_workout)
VALUES (
    1, "2021-09-03", 90, 8.5, "Too fatigued");

INSERT INTO log_set (
    workout_set_id, log_workout_id, no_reps_done,
    weight_done, rpe_done, comment_set )
VALUES (
    1,
    1,
    10,
    90,
    9,
    "Harder than expected"
);

INSERT INTO historic_pr (
    date_pr, exercise_id, no_reps_pr, weight_pr )
VALUES (
    "2021-11-22", 1, 3, 100 );