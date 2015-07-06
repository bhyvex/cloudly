/**
 * CPU Usage
 *
 * Set all action for CPU Usage chart
 * (code standards: http://javascript.crockford.com/code.html)
 */

var slashInterval = {},  // set interval globally
    mountPoint = '/';
/**
 * Call or stop interval update action (via parameter updateChart parameter)
 */
function updateslashChart(address, series, interval, duration, updateChart) {
    if (updateChart) {
        slashInterval = setInterval(function () {    // start update by duration
            requestChartData(address, series, interval, true, mountPoint)    // update chart data
        }, duration);
    } else {
        window.clearInterval(slashInterval);         // stop current interval
    }
}

/**
 * Display given chart with actual data
 */
function displayslashChart(address, chart, interval) {
    requestChartData(   // add new data to selected chart series
        address,
        chart.series,
        interval,
        false,
        mountPoint
    );
}

$(function () {
    $(document).ready(function () {
        var slashChart = new Highcharts.Chart({  // create chart object
            chart: {
                renderTo: 'slash_chart_id',
                events: {
                    load: function() {
                        updateslashChart(    // set chart first draw update action
                            addressDisks,
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
                data: []
            }]
        });

        $('#cpu_usage_interval a').on('click', function() { // catch interval change action
            var link = this,                                // create current object
                interval = $(link).attr('data-interval'),   // get interval from data attribute
                duration = setDuration(interval);           // set duration

            $('#slash_interval a.active').removeClass('active');
            $(link).addClass('active');

            updateslashChart(    // stop last ajax chart update
                addressDisks,
                slashChart.series,
                interval,
                duration,
                false
            );

            displayslashChart(   // display chart with new interval
                addressDisks,
                slashChart,
                interval
            );

            updateslashChart(    // call new interval chart ajax update
                addressDisks,
                slashChart.series,
                interval,
                duration,
                true
            );
        });

        displayslashChart(       // draw first chart
            addressDisks,
            slashChart,
            interval
        );
    });
});
