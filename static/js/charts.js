/**
 * chart.js
 *
 * Set all action for displaying charts
 */
var Chart = function () {
    return {
        address: '',
        div: '',
        mountPoint: '',
        intervalName: '',
        options: {
            update: false,
            display: false,
            interval: '3m'
        },
        chartOptions: {},
        init: function() {
            this.chart = new Highcharts.Chart(this.chartOptions);
            this.setInterval();
            this.updateActiveLink();
            this.displayChart();
            this.changeInterval();
        },
        chart: {},
        ajaxRequestData: function() {
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
                    'interval': this.options.interval,
                    'mountPoint': this.mountPoint
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
            var that = this;
            this.intervalName = setInterval(function () {
                if (that.options.display) {
                    that.ajaxRequestData();
                }
            }, that.getDuration());
        },
        setInterval: function() {
            var sessionInterval = readCookie(this.div);
            if (sessionInterval !== null) {
                this.options.interval = sessionInterval;
            }
        },
        clearInterval: function () {
            window.clearInterval(this.intervalName);
        },
        displayChart: function() {
            this.options.update = false;
            this.ajaxRequestData();
            this.updateChart();
        },
        updateChart: function() {
            this.interval();
        },
        addFirstChartData: function (data) {
            var optionalLength = 55,
                optionalData = [],
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
        updateActiveLink: function() {
            $('#' + this.div + '_interval a.active').removeClass('active');
            var link = $('#' + this.div + '_interval')
                .find('*[data-interval=' + this.options.interval + ']');
            link.addClass('active');
        },
        changeInterval: function() {
            var that = this;
            $('#' + this.div + '_interval a').on('click', function() {
                var link = this;
                that.options.interval = $(link).attr('data-interval');

                var chartSession = {};
                chartSession[that.div] = that.options.interval;
                updateSession(chartSession);

                that.updateActiveLink();
                that.clearInterval();
                that.displayChart();
            });
        }
    }
}

function getDisks() {
    var disks = $('input[name="available_disks_graphs"]').val();

    disks = disks
        .replace("]", "")
        .replace("[", "")
        .replace(/"/g, "")
        .split(",");

    var disksObj = {};
    for (i = 0; i < disks.length; ++i) {
        var diskDiv = disks[i].replace(/\//g, "slash");
        disksObj[disks[i]]  = {
            div: diskDiv,
            type: "disks"
        }
    }

    return disksObj;
}

function mergeObjects(obj1,obj2){
    var obj3 = {};

    for (var attrname in obj1) {
        obj3[attrname] = obj1[attrname];
    }

    for (var attrname in obj2) {
        obj3[attrname] = obj2[attrname];
    }

    return obj3;
}

$(document).ready(function () {
    var activeCharts = {};
    var baseChartsType = {
        "cpu_usage": {
            "div": "cpu_usage",
            "type": "cpu_usage"
        },
        "loadavg": {
            "div": "loadavg",
            "type": "loadavg"
        },
        "mem_usage": {
            "div": "mem_usage",
            "type": "mem_usage"
        },
        "inbound_traffic": {
            "div": "inbound_traffic",
            "type": "inbound_traffic"
        },
        "outbound_traffic": {
            "div": "outbound_traffic",
            "type": "outbound_traffic"
        }
    };
    var disks = getDisks();
    var serverCharts = mergeObjects(baseChartsType, disks);

    $.each(serverCharts, function(chartMp, chartType) {
        activeCharts[chartType["div"]] = new Chart();
        var chartOpt = chartOptions[chartType.type];
        chartOpt["chart"]["renderTo"] = chartType["div"];
        activeCharts[chartType["div"]]["div"] = chartType["div"];
        activeCharts[chartType["div"]]["chartOptions"] = chartOpt;
        activeCharts[chartType["div"]]["mountPoint"] = chartMp;
        activeCharts[chartType["div"]]["address"] = "/ajax/server/" + server + "/metrics/" + chartType["type"] + "/";
        activeCharts[chartType["div"]].init();
    });
});
