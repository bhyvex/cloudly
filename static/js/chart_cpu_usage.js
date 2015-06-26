/**
 * CPU Usage
 *
 * Set all action for CPU Usage chart
 * (code standards: http://javascript.crockford.com/code.html)
 */

var cpuUsageInterval = {}  // set interval globally

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

$(function () {
    $(document).ready(function () {
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
