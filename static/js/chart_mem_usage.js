/**
 * Memory Usage
 *
 * Set all action for Load Average chart
 * (code standards: http://javascript.crockford.com/code.html)
 */

var memUsageInterval = {},  // set interval globally
    optionalLength = 55;   // set optional data lenght globally

/**
 * Call or stop interval update action (via parameter updateChart parameter)
 */
function updateMemUsageChart(address, series, csrf, server, secret, interval, duration, updateChart) {
    if (updateChart) {
        memUsageInterval = setInterval(function () {    // start update by duration
            requestChartData(address, series, csrf, server, secret, interval, true)    // update chart data
        }, duration);
    } else {
        window.clearInterval(memUsageInterval);         // stop current interval
    }
}

/**
 * Call or stop interval update action (via parameter updateChart parameter)
 */
function updateMemUsageChart(address, series, csrf, server, secret, interval, duration, updateChart) {
    if (updateChart) {
        memUsageInterval = setInterval(function () {    // start update by duration
            requestChartData(address, series, csrf, server, secret, interval, true)    // update chart data
        }, duration);
    } else {
        window.clearInterval(memUsageInterval);         // stop current interval
    }
}

/**
 * Display given chart with actual data
 */
function displayMemUsageChart(address, chart, csrf, server, secret, interval) {
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

$(function () {
    $(document).ready(function () {
        var server = $('input[name="hwaddr"]').val(),           // server identifier
            csrf = $('input[name="csrfmiddlewaretoken"]').val(),// request middlevare secure
            secret = $('input[name="secret"]').val(),           // request authenticate
            interval = '3m',                                    // base interval setting
            addressMemUsage = '/ajax/server/' + server + '/metrics/mem_usage/'; // ajax call adress

        Highcharts.setOptions({ // set global chart options
            global: {
                useUTC: false   // set UTC by TSDB setting
            }
        });

        var memUsageChart = new Highcharts.Chart({  // create chart object
            chart: {
                renderTo: 'mem_usage',
                events: {
                    load: function() {
                        updateMemUsageChart(    // set chart first draw update action
                            addressMemUsage,
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
            subtitle: {
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
                    text: 'Load'
                },
                min: 0
            },
            tooltip: {
                formatter: function () {
                    return '<strong>' + Highcharts.numberFormat((this.y/1024/1000), 0, '.', ',') + ' MB ' 
                        + 'used</strong><br/>'
                        + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x*1000);
                }
            },
            series: [
                {
                    name: 'Memery Usage',
                    data: []
                }
            ]
        });
        
        $('#mem_usage_interval a').on('click', function() { // catch interval change action
            var link = this,                                // create current object
                interval = $(link).attr('data-interval'),   // get interval from data attribute
                duration = setDuration(interval);           // set duration

            updateMemUsageChart(    // stop last ajax chart update
                addressMemUsage,
                memUsageChart.series,
                csrf,
                server,
                secret,
                interval,
                duration,
                false
            );

            displayMemUsageChart(   // display chart with new interval
                addressMemUsage,
                memUsageChart,
                csrf,
                server,
                secret,
                interval
            );

            updateMemUsageChart(    // stop last ajax chart update
                addressMemUsage,
                memUsageChart.series,
                csrf,
                server,
                secret,
                interval,
                duration,
                true
            );

        });

        displayMemUsageChart(   // display chart with new interval
            addressMemUsage,
            memUsageChart,
            csrf,
            server,
            secret,
            interval
        );
    });
});
                
