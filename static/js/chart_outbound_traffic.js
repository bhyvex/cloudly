/**
 * Load Average
 *
 * Set all action for Load Average chart
 * (code standards: http://javascript.crockford.com/code.html)
 */

var outboundTrafficInterval = {},  // set interval globally
    optionalLength = 55;   // set optional data lenght globally

/**
 * Call or stop interval update action (via parameter updateChart parameter)
 */
function updateOutboundTrafficChart(address, series, csrf, server, secret, interval, duration, updateChart) {
    if (updateChart) {
        outboundTrafficInterval = setInterval(function () {    // start update by duration
            requestChartData(address, series, csrf, server, secret, interval, true)    // update chart data
        }, duration);
    } else {
        window.clearInterval(outboundTrafficInterval);         // stop current interval
    }
}

/**
 * Call or stop interval update action (via parameter updateChart parameter)
 */
function updateOutboundTrafficChart(address, series, csrf, server, secret, interval, duration, updateChart) {
    if (updateChart) {
        outboundTrafficInterval = setInterval(function () {    // start update by duration
            requestChartData(address, series, csrf, server, secret, interval, true)    // update chart data
        }, duration);
    } else {
        window.clearInterval(outboundTrafficInterval);         // stop current interval
    }
}

/**
 * Display given chart with actual data
 */
function displayOutboundTrafficChart(address, chart, csrf, server, secret, interval) {
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
            addressOutboundTraffic = '/ajax/server/' + server + '/metrics/network_output_bytes/'; // ajax call adress

        Highcharts.setOptions({ // set global chart options
            global: {
                useUTC: false   // set UTC by TSDB setting
            }
        });

        var outboundTrafficChart = new Highcharts.Chart({  // create chart object
            chart: {
                renderTo: 'outbound_traffic',
                events: {
                    load: function() {
                        updateOutboundTrafficChart(    // set chart first draw update action
                            addressOutboundTraffic,
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
                        + 'output traffic</strong><br/>'
                        + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x*1000);
                }
            },
            series: [
                {
                    name: 'Outbound Traffic',
                    data: []
                }
            ]
        });
        
        $('#outbound_traffic_interval a').on('click', function() { // catch interval change action
            var link = this,                                // create current object
                interval = $(link).attr('data-interval'),   // get interval from data attribute
                duration = setDuration(interval);           // set duration

            updateOutboundTrafficChart(    // stop last ajax chart update
                addressOutboundTraffic,
                outboundTrafficChart.series,
                csrf,
                server,
                secret,
                interval,
                duration,
                false
            );

            displayOutboundTrafficChart(   // display chart with new interval
                addressOutboundTraffic,
                outboundTrafficChart,
                csrf,
                server,
                secret,
                interval
            );

            updateOutboundTrafficChart(    // stop last ajax chart update
                addressOutboundTraffic,
                outboundTrafficChart.series,
                csrf,
                server,
                secret,
                interval,
                duration,
                true
            );

        });

        displayOutboundTrafficChart(   // display chart with new interval
            addressOutboundTraffic,
            outboundTrafficChart,
            csrf,
            server,
            secret,
            interval
        );
    });
});
                
