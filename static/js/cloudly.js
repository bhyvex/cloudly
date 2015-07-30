
var csrf = $('input[name="csrfmiddlewaretoken"]').val(),// request middlevare secure
    secret = $('input[name="secret"]').val(),           // request authenticate

    addressUpdateSession = '/ajax/session/update/';

function updateSession(values) {
    console.log(Object.prototype.toString.call(values) !== '[object Object]');
    console.log(jQuery.isEmptyObject(values));
    if (Object.prototype.toString.call(values) !== '[object Object]'
        && jQuery.isEmptyObject(values) === true
    ) {
        return false;
    }
    console.log(document.cookie);
    console.log(values);

    values.secret = secret
    $.ajax({
        "url": addressUpdateSession,
        "type": "POST",
        "dataType": "json",
        "headers": {
            'X-CSRFToken': csrf
        },
        "cache": false,
        "data": values,
        "success": function(data) {
            console.log(document.cookie);
            return true;
        },
        "error": function(data, textStatus, errorThrown) {
            console.log("error: " + textStatus);
            console.log("error: " + errorThrown);
        }
    });
}

$(document).ready(function(){
    vmsRequest.initAction();
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});
