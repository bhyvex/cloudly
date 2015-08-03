/**
 * chart.js
 *
 * Set all action for displaying charts
 */
var Chart = function () {
    return {
        address: '',
        div: '',
        intervalName: '',
        options: {
            update: false,
            display: false,
            interval: '3m'
        },
        chartOptions: {},
        init: function() {
            console.log('init');
            this.chart = new Highcharts.Chart(this.chartOptions);
            this.displayChart();
            this.changeInterval();
        },
        chart: {},
        ajaxRequestData: function() {
            console.log('ajaxRequestData');
            var that = this;
            $.ajax({
                url: this.address,
                type: 'POST',
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrf
                },
                cache: false,
                data: {
                    'server': server,
                    'secret': secret,
                    'interval': this.options.interval
                },
                success: function(data) {
                    if (data !== undefined && data !== null && data[0].length > 0) {
                        for (var i = 0; i < data.length; i++) {
                            if (that.options.update) {
                                that.chart.series[i].addPoint(data[i][0], true, true);
                            } else {
                                that.chart.series[i].setData(
                                    that.addFirstChartData(data[i])
                                );
                                that.options.display = true;
                            }
                        }
                    }
                },
                error: function(data, textStatus, errorThrown) {
                    console.log('error: ' + textStatus);
                    console.log('error: ' + errorThrown);
                }
            });
        },
        interval: function () {
            console.log('interval');
            var that = this;
            this.intervalName = setInterval(function () {
                if (that.options.display) {
                    that.ajaxRequestData();
                }
            }, that.getDuration());
        },
        clearInterval: function () {
            console.log('clearInterval');
            window.clearInterval(this.intervalName);
        },
        displayChart: function() {
            console.log('displayChart');
            this.options.update = false;
            this.ajaxRequestData();
            this.updateChart();
        },
        updateChart: function() {
            console.log('updateChart');
            this.interval();
        },
        addFirstChartData: function (data) {
            var optionalData = [],
                dataLength = data.length;

            for (var i = 0; i < (optionalLength - dataLength); i++) {
                optionalData.push([
                    (data[0][0] - (i + 1) * 3),
                    null
                ]);
            }

            optionalData = optionalData.concat(data);
            return data.reverse();
        },
        getDuration: function() {
            if (this.options.interval == '15m') {
                return '15000';
            } else if (this.options.interval == '1h') {
                return '60000';
            } else if (this.options.interval == '1d') {
                return '300000';
            } else if (this.options.interval == '7d') {
                return '1800000';
            } else if (this.options.interval == '30d') {
                return '43200000';
            } else if (this.options.interval == 'at') {
                return '1800000';
            } else {
                return '3000';
            }
        },
        changeInterval: function() {
            var that = this;
            $('#' + this.div + '_interval a').on('click', function() {
                var link = this;
                that.options.interval = $(link).attr('data-interval');

                $('#' + that.div + '_interval a.active').removeClass('active');
                $(link).addClass('active');

                that.clearInterval();
                that.displayChart();
            });
        }
    }
}


$(document).ready(function () {
    var activeCharts = {};
    var chartsType = [
        'cpu_usage',
        'loadavg',
        'mem_usage',
        'inbound_traffic',
        'outbound_traffic'
    ];

    $.each(chartsType, function(i, chartType) {
        activeCharts[chartType] = new Chart();
        activeCharts[chartType]['chartOptions'] = chartOptions[chartType];
        activeCharts[chartType]['address'] = '/ajax/server/' + server + '/metrics/' + chartType +'/';
        activeCharts[chartType]['div'] = chartType;
        activeCharts[chartType].init();
    });
});
