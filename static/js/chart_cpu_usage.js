/**
 * CPU Usage
 *
 * Set all action for CPU Usage chart
 * (code standards: http://javascript.crockford.com/code.html)
 */

var cpuUsageInterval = {},  // set interval globally
    optionalLength = 55;    // set optional data lenght globally

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

/**
 * Call or stop interval update action (via parameter updateChart parameter)
 */
function updateCpuUsageChart(address, series, csrf, server, secret, interval, duration, updateChart) {
    if (updateChart) {
        cpuUsageInterval = setInterval(function () {    // start update by duration
            requestChartData(address, series, csrf, server, secret, interval, true)    // update chart data
        }, duration);
    } else {
        window.clearInterval(cpuUsageInterval);         // stop current interval
    }
}

/**
 * Display given chart with actual data
 */
function displayCpuUsageChart(address, chart, csrf, server, secret, interval) {
    requestChartData(   // add new data to selected chart series
        address,
        chart.series,
        csrf,
        server,
        secret,
        interval,
        false
    );
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


$(function () {
    $(document).ready(function () {
        var server = $('input[name="hwaddr"]').val(),           // server identifier
            csrf = $('input[name="csrfmiddlewaretoken"]').val(),// request middlevare secure
            secret = $('input[name="secret"]').val(),           // request authenticate
            interval = '3m',                                    // base interval setting
            addressCpuUsage = '/ajax/server/' + server + '/metrics/cpu_usage/'; // ajax call adress

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
                            addressCpuUsage,
                            this.series,
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
                addressCpuUsage,
                cpuUsageChart.series,
                csrf,
                server,
                secret,
                interval,
                duration,
                false
            );

            displayCpuUsageChart(   // display chart with new interval
                addressCpuUsage,
                cpuUsageChart,
                csrf,
                server,
                secret,
                interval
            );

            updateCpuUsageChart(    // call new interval chart ajax update
                addressCpuUsage,
                cpuUsageChart.series,
                csrf,
                server,
                secret,
                interval,
                duration,
                true
            );
        });

        displayCpuUsageChart(       // draw first chart
            addressCpuUsage,
            cpuUsageChart,
            csrf,
            server,
            secret,
            interval
        );
    });
});
