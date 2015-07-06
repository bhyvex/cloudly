/**
 * Memory Usage
 *
 * Set all action for Load Average chart
 * (code standards: http://javascript.crockford.com/code.html)
 */

var memUsageInterval = {};  // set interval globally

/**
 * Call or stop interval update action (via parameter updateChart parameter)
 */
function updateMemUsageChart(address, series, interval, duration, updateChart) {
    if (updateChart) {
        memUsageInterval = setInterval(function () {    // start update by duration
            requestChartData(address, series, interval, true)    // update chart data
        }, duration);
    } else {
        window.clearInterval(memUsageInterval);         // stop current interval
    }
}

/**
 * Display given chart with actual data
 */
function displayMemUsageChart(address, chart, interval) {
    requestChartData(   // add new data to selected chart series
        address,
        chart.series,
        interval,
        false
    );
}

$(function () {
    $(document).ready(function () {
        var memUsageChart = new Highcharts.Chart({  // create chart object
            chart: {
                renderTo: 'mem_usage',
                events: {
                    load: function() {
                        updateMemUsageChart(    // set chart first draw update action
                            addressMemUsage,
                            this.series,
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
                    text: 'Memory'
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

            $('#mem_usage_interval a.active').removeClass('active');
            $(link).addClass('active');

            updateMemUsageChart(    // stop last ajax chart update
                addressMemUsage,
                memUsageChart.series,
                interval,
                duration,
                false
            );

            displayMemUsageChart(   // display chart with new interval
                addressMemUsage,
                memUsageChart,
                interval
            );

            updateMemUsageChart(    // stop last ajax chart update
                addressMemUsage,
                memUsageChart.series,
                interval,
                duration,
                true
            );

        });

        displayMemUsageChart(   // display chart with new interval
            addressMemUsage,
            memUsageChart,
            interval
        );
    });
});

