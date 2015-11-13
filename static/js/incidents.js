
function updateIncidents() {
    console.log(secret);
    $.ajax({
        url: '/ajax/incidents/',
        type: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken': csrf
        },
        cache: false,
        data: {
            "secret": secret
        },
        success: function(data) {
            console.log(data);
        },
        error: function(data, textStatus, errorThrown) {
            console.log('error: ' + textStatus);
            console.log('error: ' + errorThrown);
        }
    });
}

$(document).ready(function() {
    updateIncidents();
});
