$(function () {
    $(document).ready(function () {
        var server = $('input[name="hwaddr"]').val();
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        var secret = $('input[name="secret"]').val();

        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });

        var interval = '3m';
        var duration = '3s';
        cpu_usage_set(csrf, server, secret, interval, duration);
        $('#cpu_usage_interval a').on('click', function() {
            var link = this;
            interval = $(link).attr('data-interval');
            duration = $(link).attr('data-duration');
            console.log('click');
            console.log(interval);
            console.log(duration);
            cpu_usage_set(csrf, server, secret, interval, duration);
        });
    });
});

function cpu_usage_set(csrf, server, secret, interval, duration) {
    var address = '/ajax/server/' + server + '/metrics/cpu_usage/';

    function requestCpuUsageData(series, csrf, server, secret) {
        var address = '/ajax/server/' + server + '/metrics/cpu_usage/';
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
                'duration': duration,
                'interval': interval
            },
            success: function(data) {
                series.addPoint(data[0], true, true);
            },
            error: function(data, textStatus, errorThrown) {
                console.log('error: ' + textStatus);
                console.log('error: ' + errorThrown);
            }
        });
    }

    if (interval == '3m') {
        var timeout = '3000';
    } else if (interval == '15m') {
        var timeout = '15000';
    } else if (interval == '1h') {
        var timeout = '60000';
    }

    function updateCpuUsageChart(series, csrf, server, secret)
    {
        setInterval(function() {
            requestCpuUsageData(series, csrf, server, secret);
        }, timeout);
    }

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
            'interval': interval,
            'duration': duration
        },
        success: function(data) {
            if (data != null) {
                var optionalData = [];
                var optionalLength = 55;
                console.log(data);
                var dataLength = data.length;
                for(var i = 0; i < (optionalLength - dataLength); i++) {
                    optionalData.push([
                            (data[0][0] - (i + 1) * 5),
                            null
                        ]);
                }
                optionalData = optionalData.concat(data);
                var cpuUsageChart = new Highcharts.Chart({
                    chart: {
                        renderTo: 'cpu_usage',
                        events: {
                            load: function() {
                                updateCpuUsageChart(
                                    this.series[0],
                                    csrf,
                                    server,
                                    secret
                                );
                            }
                        }
                    },
                    xAxis: {
                        type: 'datetime',
                        labels: {
                            formatter: function() {
                                return Highcharts.dateFormat('%H:%M:%S', this.value * 1000);
                            }
                        }
                    },
                    yAxis: {
                        title: {
                            text: 'Value'
                        },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'
                    }]
                    },
                    tooltip: {
                        formatter: function () {
                            return '<b>' + Highcharts.numberFormat(this.y, 0) + this.series.name + '</b><br/>' +
                                Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x*1000);

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
                        data: optionalData.reverse(),
                        zones: [{
                                value: 10,
                                color: '#7cb5ec'
                            }, {
                                value: 80,
                                color: '#90ed7d'
                            },{
                                value: 95,
                                color: 'orange'
                            },{
                                color: 'red'
                            }
                        ]
                    }]
                });
            }
        },
        error: function(data, textStatus, errorThrown) {
            console.log('error: ' + textStatus);
            console.log('error: ' + errorThrown);
        }
    });
}

function loadavg_set (csrf, server, secret)
{
    /*
    function requestLoadAvgData(series, csrf, server, secret) {
        var address = '/ajax/server/' + server + '/metrics/loadavg/';
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
            'secret': secret
            },
            success: function(data) {
                if (typeof element === 'undefined') {
                    var element = [null,null];
                }

                if (element[0] != data[0]) {
                    series.addPoint(data[0], true, true);
                }

                element [0] = data [0];
            },
            error: function(data, textStatus, errorThrown) {
                console.log('error: ' + textStatus);
                console.log('error: ' + errorThrown);
            }
        });
    }

    function updateLoadAvgChart(series, csrf, server, secret) {
        setInterval(function() {
            requestLoadAvgData(series, csrf, server, secret);
        }, 1000);
    }

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
            'secret': secret
        },
        success: function(data) {
            var cpuUsageChart = new Highcharts.Chart({
                chart: {
                    renderTo: 'cpu_usage',
            events: {
                load: function() {
                    updateChart(this.series[0], csrf, server, secret);
                }
            }
                },
            title: {
                text: 'CPU Usage'
            },
            xAxis: {
                type: 'datetime',
            },
            yAxis: {
                title: {
                    text: 'Value'
                },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
            },
            tooltip: {
                formatter: function () {
                    return '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                        Highcharts.numberFormat(this.y, 2);
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: '%CPU Usage',
                data: data.reverse()
            }]
            });
        },
        error: function(data, textStatus, errorThrown) {
            console.log('error: ' + textStatus);
            console.log('error: ' + errorThrown);
        }
    });
    */
}
