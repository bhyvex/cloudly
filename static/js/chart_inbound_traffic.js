/**
 * Load Average
 *
 * Set all action for Load Average chart
 * (code standards: http://javascript.crockford.com/code.html)
 */

var inboundTrafficInterval = {};  // set interval globally

/**
 * Call or stop interval update action (via parameter updateChart parameter)
 */
function updateInboundTrafficChart(address, series, interval, duration, updateChart) {
    if (updateChart) {
        inboundTrafficInterval = setInterval(function () {    // start update by duration
            requestChartData(address, series, interval, true)    // update chart data
        }, duration);
    } else {
        window.clearInterval(inboundTrafficInterval);         // stop current interval
    }
}

/**
 * Display given chart with actual data
 */
function displayInboundTrafficChart(address, chart, interval) {
    requestChartData(   // add new data to selected chart series
        address,
        chart.series,
        interval,
        false
    );
}

$(function () {
    $(document).ready(function () {
        var inboundTrafficChart = new Highcharts.Chart({  // create chart object
            chart: {
                renderTo: 'inbound_traffic',
                events: {
                    load: function() {
                        updateInboundTrafficChart(    // set chart first draw update action
                            addressInboundTraffic,
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
                    return '<strong>' + Highcharts.numberFormat(this.y/1024, 0, '.', ',') + ' KB/s '
                        + 'input traffic</strong><br/>'
                        + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x*1000);
                }
            },
            series: [
                {
                    name: 'Inbound Traffic',
                    data: []
                }
            ]
        });

        $('#inbound_traffic_interval a').on('click', function() { // catch interval change action
            var link = this,                                // create current object
                interval = $(link).attr('data-interval'),   // get interval from data attribute
                duration = setDuration(interval);           // set duration

            $('#inbound_traffic_interval a.active').removeClass('active');
            $(link).addClass('active');

            updateInboundTrafficChart(    // stop last ajax chart update
                addressInboundTraffic,
                inboundTrafficChart.series,
                interval,
                duration,
                false
            );

            displayInboundTrafficChart(   // display chart with new interval
                addressInboundTraffic,
                inboundTrafficChart,
                interval
            );

            updateInboundTrafficChart(    // stop last ajax chart update
                addressInboundTraffic,
                inboundTrafficChart.series,
                interval,
                duration,
                true
            );

        });

        displayInboundTrafficChart(   // display chart with new interval
            addressInboundTraffic,
            inboundTrafficChart,
            interval
        );
    });
});

