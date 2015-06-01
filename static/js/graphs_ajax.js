$(function () {
    $(document).ready(function () {
        var server = $('input[name="hwaddr"]').val();
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        var secret = $('input[name="secret"]').val();
        var address = '/ajax/server/' + server + '/metrics/cpu_usage/';

        function requestCpuUsageData(series) {
            $.ajax({
                url: address,
                type: 'POST',
                dataType: 'json',
                headers: {
                    //         'X-CSRFToken': csrf
                },
                cache: false,
                data: {
                    //         'server': server,
                    //         'secret': secret
                },
                success: function(data) {
                    series.addPoint(data[0], true, true);
                }
            });
        }

        function updateChart(series) {
            setInterval(function() {
                requestCpuUsageData(series, 'point');
            }, 1000);
        }

        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });

        $.ajax({
            url: address,
            type: 'POST',
            dataType: 'json',
            headers: {
                //         'X-CSRFToken': csrf
            },
            cache: false,
            data: {
                //         'server': server,
                //         'secret': secret
            },
            success: function(data) {
                var cpuUsageChart = new Highcharts.Chart({
                    chart: {
                        renderTo: 'cpu_usage',
                        type: 'spline',
                        marginRight: 10,
                        events: {
                            load: function() {
                                updateChart(this.series[0]);
                            }
                        }
                    },
                    title: {
                        text: 'Live random data'
                    },
                    xAxis: {
                        type: 'datetime',
                        tickPixelInterval: 150
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
                        name: 'Random data',
                        data: data
                    }]
                });
            }
        });
    });
});
