
var server = $('input[name="hwaddr"]').val(),           // server identifier
    csrf = $('input[name="csrfmiddlewaretoken"]').val(),// request middlevare secure
    secret = $('input[name="secret"]').val(),           // request authenticate
    interval = '3m',                                    // base interval setting
    optionalLength = 55,                                // set optional data lenght globally
    addressServerInfo = '/ajax/server/' + server + '/metrics/server_info/', // ajax call adress
    addressLoadavg = '/ajax/server/' + server + '/metrics/loadavg/', // ajax call adress
    addressCpuUsage = '/ajax/server/' + server + '/metrics/cpu_usage/', // ajax call adress
    addressMemUsage = '/ajax/server/' + server + '/metrics/mem_usage/'; // ajax call adress
    addressOutboundTraffic = '/ajax/server/' + server + '/metrics/network_output_bytes/', // ajax call adress
    addressInboundTraffic = '/ajax/server/' + server + '/metrics/network_input_bytes/'; // ajax call adress

(function($) { 
    $.fn.deactivePanel = function() {
        this    
            .find('.btn-minimize')
            .find('i')
            .attr('class','fa fa-chevron-down');

        this
            .find('.panel-body')
            .css('display','none');
    };
})(jQuery);

(function($) { 
    $.fn.updateProgressBar = function(data) {
        console.log(this);
    };
})(jQuery);

function updateServerInfo(csrf, server, secret) {
    console.log(csrf);
    $.ajax({
        url: addressServerInfo,
        type: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken': csrf
        },
        cache: false,
        data: {
            'server': server,
            'secret': secret
        },
        success: function(data) {
            console.log(data);
            $('.cpu_usage_progess_bar').updateProgressBar(data);
        },
        error: function(data, textStatus, errorThrown) {
            console.log('error: ' + textStatus);
            console.log('error: ' + errorThrown);
        }
    });

};

/**
 * Set duration by interval value
 */
function setDuration(interval) {
    var duration = '3000';      // base duration value
    if (interval == '15m') {
        duration = '15000';
    } else if (interval == '1h') {
        duration = '60000';
    } else if (interval == '1d') {
        duration = '300000';
    } else if (interval == '7d') {
        duration = '1800000';
    } else if (interval == '30d') {
        duration = '43200000';
    } else if (interval == 'at') {
        duration = '1800000';
    }
    return duration;
}

/**
 * Get new data via ajax call and set it to given serie
 */
function requestChartData(address, series, csrf, server, secret, interval, updateChart) {
    $.ajax({
        url: address,
        type: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken': csrf
        },
        cache: false,
        data: {
            'server': server,
            'secret': secret,
            'interval': interval
        },
        success: function(data) {
            if (data !== undefined && data !== null && data[0].length > 0) {
                for (var i = 0; i < data.length; i++) {
                    if (updateChart) {
                        series[i].addPoint(data[i][0], true, true);   // add new point to chart serie
                    } else {
                        series[i].setData(addFirstChartData(data[i])) // add data set to chart serie
                    }
                }
            }
        },
        error: function(data, textStatus, errorThrown) {
            console.log('error: ' + textStatus);
            console.log('error: ' + errorThrown);
        }
    });
}

/**
 * Check, fill and sort given data with global parametrs
 */
function addFirstChartData(data) {
    var optionalData = [],          // empty optional data array
        dataLength = data.length;   // current data lenght

    for (var i = 0; i < (optionalLength - dataLength); i++) {
        optionalData.push([
            (data[0][0] - (i + 1) * 3), // set timestamp value
            null                        // set cpu usage value
        ]);
    }

    optionalData = optionalData.concat(data);   // fill data to optional lenght
    return data.reverse();          // chart need reverted data
}

$(document).ready(function() {
    $('#diskGraphs').deactivePanel();
    $('#serviceDiscovery').deactivePanel();
    $('#serverActivity').deactivePanel();
    
    Highcharts.setOptions({ // set global chart options
        global: {
            useUTC: false   // set UTC by TSDB setting
        }
    });

    updateServerInfo(csrf, server, secret);
});

