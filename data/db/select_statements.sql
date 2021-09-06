SELECT e.exercise_desc,
       ws.set_id,
       ws.no_reps,
       ws.perc_rm,
       ws.min_rpe,
       ws.max_rpe,
       p.program_desc,
       b.block_desc,
       w.week,
       w.day
FROM workout_set ws 
    LEFT JOIN exercise e 
        ON ws.exercise_id = e.exercise_id
    LEFT JOIN workout w
        ON ws.workout_id = w.workout_id
    LEFT JOIN block b
        ON w.block_id = b.block_id
    LEFT JOIN program p
        ON b.program_id = p.program_id;
       