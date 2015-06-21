/**
 * Load Average
 *
 * Set all action for Load Average chart
 * (code standards: http://javascript.crockford.com/code.html)
 */

var loadavgInterval = {},  // set interval globally
    optionalLength = 55;   // set optional data lenght globally

/**
 * Call or stop interval update action (via parameter updateChart parameter)
 */
function updateLoadAvgChart(address, series, csrf, server, secret, interval, duration, updateChart) {
    if (updateChart) {
        loadavgInterval = setInterval(function () {    // start update by duration
            requestChartData(address, series, csrf, server, secret, interval, true)    // update chart data
        }, duration);
    } else {
        window.clearInterval(loadavgInterval);         // stop current interval
    }
}

/**
 * Call or stop interval update action (via parameter updateChart parameter)
 */
function updateLoadavgChart(address, series, csrf, server, secret, interval, duration, updateChart) {
    if (updateChart) {
        loadavgInterval = setInterval(function () {    // start update by duration
            requestChartData(address, series, csrf, server, secret, interval, true)    // update chart data
        }, duration);
    } else {
        window.clearInterval(loadavgInterval);         // stop current interval
    }
}

/**
 * Display given chart with actual data
 */
function displayLoadavgChart(address, chart, csrf, server, secret, interval) {
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
            addressLoadavg = '/ajax/server/' + server + '/metrics/loadavg/'; // ajax call adress

        Highcharts.setOptions({ // set global chart options
            global: {
                useUTC: false   // set UTC by TSDB setting
            }
        });

        var loadavgChart = new Highcharts.Chart({  // create chart object
            chart: {
                renderTo: 'loadavg',
                events: {
                    load: function() {
                        updateLoadAvgChart(    // set chart first draw update action
                            addressLoadavg,
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
                text: 'Server Load Average'
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
                    return '<b>' + Highcharts.numberFormat(this.y, 0)
                        + this.series.name + '</b><br/>'
                        + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x*1000);

                }
            },
            series: [
                {
                    name: '1-min',
                    data: []
                }, 
                {
                    name: '5-mins',
                    data: []
                }, 
                {
                    name: '15-mins',
                    data: []
                }
            ]
        });
        
        $('#loadavg_interval a').on('click', function() { // catch interval change action
            var link = this,                                // create current object
                interval = $(link).attr('data-interval'),   // get interval from data attribute
                duration = setDuration(interval);           // set duration

            updateLoadavgChart(    // stop last ajax chart update
                addressLoadavg,
                loadavgChart.series,
                csrf,
                server,
                secret,
                interval,
                duration,
                false
            );

            displayLoadavgChart(   // display chart with new interval
                addressLoadavg,
                loadavgChart,
                csrf,
                server,
                secret,
                interval
            );

            updateLoadavgChart(    // stop last ajax chart update
                addressLoadavg,
                loadavgChart.series,
                csrf,
                server,
                secret,
                interval,
                duration,
                true
            );

        });

        displayLoadavgChart(   // display chart with new interval
            addressLoadavg,
            loadavgChart,
            csrf,
            server,
            secret,
            interval
        );
    });
});
                
