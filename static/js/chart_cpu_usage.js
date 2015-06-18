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
            series.addPoint(data[0], true, true);   // add new point to chart serie
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
function updateCpuUsageChart(series, csrf, server, secret, interval, duration, updateChart) {
    if (updateChart) {
        cpuUsageInterval = setInterval(function () {    // start update by duration
            requestCpuUsageChartData(series, csrf, server, secret, interval)    // update chart data
        }, duration);
    } else {
        window.clearInterval(cpuUsageInterval);         // stop current interval
    }
}

/**
 * Display given chart with actual data
 */
function displayCpuUsageChart(chart, csrf, server, secret, interval) {
    var address = '/ajax/server/' + server + '/metrics/cpu_usage/'; // ajax call adress

    $.ajax({    // ajax for actual chart data
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
            if (data != null) {                 // check data and fill if needed
                var optionalData = [],          // empty optional data array
                    optionalLength = 55,        // optional data lenght
                    dataLength = data.length;   // current data lenght

                for (var i = 0; i < (optionalLength - dataLength); i++) {
                    optionalData.push([
                        (data[0][0] - (i + 1) * 3), // set timestamp value
                        null                        // set cpu usage value
                    ]);
                }

                optionalData = optionalData.concat(data);   // fill data to optional lenght
                chart.series[0].setData(data.reverse());    // chart need reverted data
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

        Highcharts.setOptions({ // set global chart options
            global: {
                useUTC: false   // set UTC by TSDB setting
            }
        });

        var cpuUsageChart = new Highcharts.Chart({  // create chart object
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
                        return Highcharts.dateFormat('%H:%M:%S', this.value * 1000);    // chart need value in milisecond
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
                zones: [    // set zones color setting
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

        $('#cpu_usage_interval a').on('click', function() { // catch interval change action
            var link = this,                                // create current object
                interval = $(link).attr('data-interval'),   // get interval from data attribute
                duration = setDuration(interval);           // set duration

            updateCpuUsageChart(    // stop last ajax chart update
                cpuUsageChart.series[0],
                csrf,
                server,
                secret,
                interval,
                duration,
                false
            );

            displayCpuUsageChart(   // display chart with new interval
                cpuUsageChart,
                csrf,
                server,
                secret,
                interval,
                duration
            );

            updateCpuUsageChart(    // call new interval chart ajax update
                cpuUsageChart.series[0],
                csrf,
                server,
                secret,
                interval,
                duration,
                true
            );
        });

        displayCpuUsageChart(       // draw first chart
            cpuUsageChart,
            csrf,
            server,
            secret,
            interval,
            setDuration(interval)
        );
    });
});
