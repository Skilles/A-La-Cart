const mealsDiv = document.getElementById('meals');

function addBreakfastToPlan() {
    var breakfast = document.getElementById('breakfast');
    var id = breakfast.value;
    $.post('', {
        'recipe_id': id,
        'type': 'breakfast'
    }, function (data) {
        if (data.success) {
            breakfast.hidden = true;
        }
    });
}

function addLunchToPlan() {
    var lunch = document.getElementById('lunch');
    var id = lunch.value;
    $.post('', {
        'recipe_id': id,
        'type': 'lunch'
    }, function (data) {
        if (data.success) {
            lunch.hidden = true;
        }
    });
}

function addDinnerToPlan() {
    var dinner = document.getElementById('dinner');
    var id = dinner.value;
    $.post('', {
        'recipe_id': id,
        'type': 'dinner'
    }, function (data) {
        if (data.success) {
            dinner.hidden = true;
        }
    });
}