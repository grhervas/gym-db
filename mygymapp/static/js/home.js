/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/programs',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(program) {
            let ajax_options = {
                type: 'POST',
                url: 'api/programs',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(program)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(program) {
            let ajax_options = {
                type: 'PUT',
                url: `api/programs/${program.program_id}`,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(program)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'delete': function(program_id) {
            let ajax_options = {
                type: 'DELETE',
                url: `api/programs/${program_id}`,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $program_id = $('#program_id'),
        $program_desc = $('#program_desc'),
        $date_start = $('#date_start'),
        $date_end = $('#date_en'),
        $objective = $('#objective');

    // return the API
    return {
        reset: function() {
            $program_id.val('');
            $program_desc.val('').focus();
            $date_start.val('');
            $date_end.val('');
            $objective.val('');
        },
        update_editor: function(program) {
            $program_id.val(program.program_id);
            $program_desc.val(program.program_desc).focus();
            $date_start.val(program.date_start);
            $date_end.val(program.date_end);
            $objective.val(program.objective);
        },
        build_table: function(programs) {
            let rows = ''

            // clear the table
            $('.programs table > tbody').empty();

            // did we get a programs array?
            if (programs) {
                for (let i=0, l=programs.length; i < l; i++) {
                    rows += `<tr data-program-id="${programs[i].program_id}">
                        <td class="program_desc">${programs[i].program_desc}</td>
                        <td class="date_start">${programs[i].date_start}</td>
                        <td class="date_end">${programs[i].date_end}</td>
                        <td class="objective">${programs[i].objective}</td>
                    </tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $program_id = $('#program_id'),
        $program_desc = $('#program_desc'),
        $date_start = $('#date_start'),
        $date_end = $('#date_end'),
        $objective = $('#objective');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(program_desc, date_start, date_end) {
        return program_desc !== "" && date_start < date_end;
    }

    // Create our event handlers
    $('#create').click(function(e) {
        let program_desc = $program_desc.val(),
            date_start = $date_start.val(),
            date_end = $date_end.val(),
            objective = $objective.val();

        e.preventDefault();

        if (validate(program_desc, date_start, date_end)) {
            model.create({
                'program_desc': program_desc,
                'date_start': date_start,
                'date_end': date_end,
                'objective': objective
            })
        } else {
            alert('Problem with Program input');
        }
    });

    $('#update').click(function(e) {
        let program_id = $program_id.val(),
            program_desc = $program_desc.val(),
            date_start = $date_start.val(),
            date_end = $date_end.val(),
            objective = $objective.val();

        e.preventDefault();

        if (validate(program_desc, date_start, date_end)) {
            model.update({
                program_id: program_id,
                program_desc: program_desc,
                date_start: date_start,
                date_end: date_end,
                objective: objective
            })
        } else {
            alert('Problem with Program input');
        }
        e.preventDefault();
    });

    $('#delete').click(function(e) {
        let program_id = $program_id.val();

        e.preventDefault();

        if (validate('placeholder', program_id)) {
            model.delete(program_id)
        } else {
            alert('Problem with Program name input');
        }
        e.preventDefault();
    });

    $('#reset').click(function() {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            program_id,
            program_desc,
            date_start,
            date_end,
            objective;

        program_id = $target
            .parent()
            .attr('data-program-id');

        program_desc = $target
            .parent()
            .find('td.program_desc')
            .text();

        date_start = $target
            .parent()
            .find('td.date_start')
            .text();

        date_end = $target
            .parent()
            .find('td.date_end')
            .text();

        objective = $target
            .parent()
            .find('td.objective')
            .text();

        view.update_editor({
            program_id: program_id,
            program_desc: program_desc,
            date_start: date_start,
            date_end: date_end,
            objective: objective
        });
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));

