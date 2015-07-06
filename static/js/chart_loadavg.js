/**
 * Load Average
 *
 * Set all action for Load Average chart
 * (code standards: http://javascript.crockford.com/code.html)
 */

var loadavgInterval = {};  // set interval globally

/**
 * Call or stop interval update action (via parameter updateChart parameter)
 */
function updateLoadavgChart(address, series, interval, duration, updateChart) {
    if (updateChart) {
        loadavgInterval = setInterval(function () {    // start update by duration
            requestChartData(address, series, interval, true)    // update chart data
        }, duration);
    } else {
        window.clearInterval(loadavgInterval);         // stop current interval
    }
}

/**
 * Display given chart with actual data
 */
function displayLoadavgChart(address, chart, interval) {
    requestChartData(   // add new data to selected chart series
        address,
        chart.series,
        interval,
        false
    );
}

$(function () {
    $(document).ready(function () {
        var loadavgChart = new Highcharts.Chart({  // create chart object
            chart: {
                renderTo: 'loadavg',
                events: {
                    load: function() {
                        updateLoadavgChart(    // set chart first draw update action
                            addressLoadavg,
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
                    text: 'Load'
                },
                min: 0
            },
            tooltip: {
                formatter: function () {
                    return '<strong>' + Highcharts.numberFormat(this.y, 2,'.',',')
                        + ' in average</strong> (' + this.series.name + ')<br/>'
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

            $('#loadavg_interval a.active').removeClass('active');
            $(link).addClass('active');

            updateLoadavgChart(    // stop last ajax chart update
                addressLoadavg,
                loadavgChart.series,
                interval,
                duration,
                false
            );

            displayLoadavgChart(   // display chart with new interval
                addressLoadavg,
                loadavgChart,
                interval
            );

            updateLoadavgChart(    // stop last ajax chart update
                addressLoadavg,
                loadavgChart.series,
                interval,
                duration,
                true
            );

        });

        displayLoadavgChart(   // display chart with new interval
            addressLoadavg,
            loadavgChart,
            interval
        );
    });
});

