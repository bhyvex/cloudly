var server = $('input[name="hwaddr"]').val();
var csrf = $('input[name="csrfmiddlewaretoken"]').val();
var secret = $('input[name="secret"]').val();

function requestCpuUsageData() {
    var address = '/ajax/server/' + server + '/metrics/cpu_usage/';

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
            'secret': secret
        },
        success: function(point) {
            var series = cpuUsagechart.series[0];
            var shift = series.data.length > 60;

            // add the point
            cpuUsagechart.series[0].addPoint(point, true, shift);

            // call it again after one second
            setTimeout(requestCpuUsageData, 1000);
        }
    });
}

$(document).ready(function() {
    var cpuUsagechart = new Highcharts.Chart({
        chart: {
            renderTo: '#cpu_usage',
            type: 'spline',
            events: {
                load: requestCpuUsageData
            }
        },
        title: {
            text: 'CPU Usage'
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            type: 'datetime',
            title: {
                text: 'Datetime'
            }
        },
        yAxis: {
            title: {
                text: 'CPU %'
            },
        },
        min: 0,
        tooltip: {
            headerFormat: '<b>{series.name}:</b> {point.y:.2f}<br>',
            pointFormat: '{point.x:%Y-%m-%d %H:%M:%S}'
        },
        series: [{
            name: 'CPU Used',
            data: []
        }]
    });
});
