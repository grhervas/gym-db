INSERT INTO program (
    program_desc, 
    date_start,
    date_end,
    objective)
VALUES (
    "PHAT v2 (abr'21')",
    "01/04/2021",
    "01/07/2021",
    "Hypertrophy (+3kg)");

INSERT INTO block (
    block_desc,
    program_id )
VALUES (
    "Volume_1",
    1 );

INSERT INTO workout (
    block_id,
    week,
    day )
VALUES (
    1,
    1,
    3 );

INSERT INTO exercise (
    exercise_desc)
VALUES (
    "bench press");

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
    8,
    7 );

INSERT INTO log_workout(
    workout_id, date_workout, duration_min, intensity, comment_workout)
VALUES (
    1, "2021-09-03", 90, 8.5, "Too fatigued");