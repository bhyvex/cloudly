
var server = $('input[name="hwaddr"]').val(),           // server identifier
    csrf = $('input[name="csrfmiddlewaretoken"]').val(),// request middlevare secure
    secret = $('input[name="secret"]').val(),           // request authenticate

    addressUpdateSession ='ajax/session/update/';

function updateSession(values) {
    console.log(document.cookie);
    if (Object.prototype.toString.call(values) !== '[object Object]'
        || jQuery.isEmptyObject(values) === false
    ) {
        return false;
    }

    $.ajax({
        "url": addressUpdateSession,
        "type": "POST",
        "dataType": "json",
        "headers": {
            'X-CSRFToken': csrf
        },
        "cache": false,
        "data": {
            "server": server,
            "secret": secret,
            "values": values
        },
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
