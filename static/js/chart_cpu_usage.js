/**
 * CPU Usage
 *
 * Set all action for CPU Usage chart
 * (code standards: http://javascript.crockford.com/code.html)
 */

var cpuUsageInterval = {};  // set interval globally

/**
 * Get new data via ajax call and set it to given serie
 */
function requestCpuUsageChartData(series, csrf, server, secret, interval) {
    var address = '/ajax/server/' + server + '/metrics/cpu_usage/'; // ajax call adress

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
            series.addPoint(data[0], true, true);
        },
        error: function(data, textStatus, errorThrown) {
            // console.log('error: ' + textStatus);
            // console.log('error: ' + errorThrown);
        }
    });
}

/**
 * Call or stop interval update action (via parameter updateChart parameter)
 */
function updateCpuUsageChart(series, csrf, server, secret, interval, timeout, updateChart) {
    if (updateChart) {
        cpuUsageInterval = setInterval(function () {
            requestCpuUsageChartData(series, csrf, server, secret, interval)
        }, timeout);
    } else {
        window.clearInterval(cpuUsageInterval);
    }
}

/**
 * Display given chart with actual data
 */
function displayCpuUsageChart(chart, csrf, server, secret, interval) {
    var address = '/ajax/server/' + server + '/metrics/cpu_usage/'; // ajax call adress

    // ajax for actual chart data
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
            if (data != null) {
                var optionalData = [],
                    optionalLength = 55,
                    dataLength = data.length;

                for (var i = 0; i < (optionalLength - dataLength); i++) {
                    optionalData.push([
                        (data[0][0] - (i + 1) * 5),
                        null
                    ]);
                }

                optionalData = optionalData.concat(data);
                chart.series[0].setData(data.reverse());
            }
        },
        error: function(data, textStatus, errorThrown) {
            // console.log('error: ' + textStatus);
            // console.log('error: ' + errorThrown);
        }
    });
}

/**
 * Set duration by interval value
 */
function setDuration(interval) {
    var duration = '3000';      // base duration value
    if (interval == '15m') {
        duration = '15000';
    } else if (interval == '1h') {
        duration = '60000';
    }
    return duration;
}


$(function () {
    $(document).ready(function () {
        var server = $('input[name="hwaddr"]').val(),           // server identifier
            csrf = $('input[name="csrfmiddlewaretoken"]').val(),// request middlevare secure
            secret = $('input[name="secret"]').val(),           // request authenticate
            interval = '3m';                                    // base interval setting

        // set global chart options
        Highcharts.setOptions({
            global: {
                useUTC: false   // set for TSDB
            }
        });

        // create chart object
        var cpuUsageChart = new Highcharts.Chart({
            chart: {
                renderTo: 'cpu_usage',
                events: {
                    load: function() {
                        updateCpuUsageChart(    // set chart first draw update action
                            this.series[0],
                            csrf,
                            server,
                            secret,
                            interval,
                            setDuration(interval),
                            true
                       );
                    }
                }
            },
            title: {
                text: ''
            },
            xAxis: {
                type: 'datetime',
                labels: {
                    formatter: function() {
                        return Highcharts.dateFormat('%H:%M:%S', this.value * 1000);
                    }
                }
            },
            yAxis: {
                title: {
                    text: 'CPU Usage value %'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function () {
                    return '<b>' + Highcharts.numberFormat(this.y, 0)
                        + this.series.name + '</b><br/>'
                        + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x*1000);

                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: '% CPU used',
                data: [],
                zones: [
                    {
                        value: 10,
                        color: '#7cb5ec'
                    },
                    {
                        value: 80,
                        color: '#90ed7d'
                    },
                    {
                        value: 95,
                        color: 'orange'
                    },
                    {
                        color: 'red'
                    }
                ]
            }]
        });

        // check update interval action
        $('#cpu_usage_interval a').on('click', function() {
            var link = this,                                // create current object
                interval = $(link).attr('data-interval'),   // get interval from data attribute
                duration = setDuration(interval);           // set duration

            // stop last ajax chart update
            updateCpuUsageChart(
                cpuUsageChart,
                csrf,
                server,
                secret,
                interval,
                duration,
                false
            );

            // display chart with new interval
            displayCpuUsageChart(
                cpuUsageChart,
                csrf,
                server,
                secret,
                interval,
                duration
            );

            // call new interval chart ajax update
            updateCpuUsageChart(
                cpuUsageChart.series[0],
                csrf,
                server,
                secret,
                interval,
                duration,
                true
            );
        });

        // draw chart
        displayCpuUsageChart(
            cpuUsageChart,
            csrf,
            server,
            secret,
            interval,
            setDuration(interval)
        );
    });
});
