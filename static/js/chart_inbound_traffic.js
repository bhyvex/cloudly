/**
 * Load Average
 *
 * Set all action for Load Average chart
 * (code standards: http://javascript.crockford.com/code.html)
 */

var inboundTrafficInterval = {},  // set interval globally
    optionalLength = 55;   // set optional data lenght globally

/**
 * Call or stop interval update action (via parameter updateChart parameter)
 */
function updateInboundTrafficChart(address, series, csrf, server, secret, interval, duration, updateChart) {
    if (updateChart) {
        inboundTrafficInterval = setInterval(function () {    // start update by duration
            requestChartData(address, series, csrf, server, secret, interval, true)    // update chart data
        }, duration);
    } else {
        window.clearInterval(inboundTrafficInterval);         // stop current interval
    }
}

/**
 * Call or stop interval update action (via parameter updateChart parameter)
 */
function updateInboundTrafficChart(address, series, csrf, server, secret, interval, duration, updateChart) {
    if (updateChart) {
        inboundTrafficInterval = setInterval(function () {    // start update by duration
            requestChartData(address, series, csrf, server, secret, interval, true)    // update chart data
        }, duration);
    } else {
        window.clearInterval(inboundTrafficInterval);         // stop current interval
    }
}

/**
 * Display given chart with actual data
 */
function displayInboundTrafficChart(address, chart, csrf, server, secret, interval) {
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
        console.log('aksdjhfkasjdhfkashdfiuhweIUFHAS');
        var server = $('input[name="hwaddr"]').val(),           // server identifier
            csrf = $('input[name="csrfmiddlewaretoken"]').val(),// request middlevare secure
            secret = $('input[name="secret"]').val(),           // request authenticate
            interval = '3m',                                    // base interval setting
            addressInboundTraffic = '/ajax/server/' + server + '/metrics/network_input_bytes/'; // ajax call adress

        Highcharts.setOptions({ // set global chart options
            global: {
                useUTC: false   // set UTC by TSDB setting
            }
        });

        var inboundTrafficChart = new Highcharts.Chart({  // create chart object
            chart: {
                renderTo: 'inbound_traffic',
                events: {
                    load: function() {
                        updateInboundTrafficChart(    // set chart first draw update action
                            addressInboundTraffic,
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

            updateInboundTrafficChart(    // stop last ajax chart update
                addressInboundTraffic,
                inboundTrafficChart.series,
                csrf,
                server,
                secret,
                interval,
                duration,
                false
            );

            displayInboundTrafficChart(   // display chart with new interval
                addressInboundTraffic,
                inboundTrafficChart,
                csrf,
                server,
                secret,
                interval
            );

            updateInboundTrafficChart(    // stop last ajax chart update
                addressInboundTraffic,
                inboundTrafficChart.series,
                csrf,
                server,
                secret,
                interval,
                duration,
                true
            );

        });

        displayInboundTrafficChart(   // display chart with new interval
            addressInboundTraffic,
            inboundTrafficChart,
            csrf,
            server,
            secret,
            interval
        );
    });
});
                
