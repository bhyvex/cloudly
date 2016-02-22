/**
 * Set chart base options by type
 */

/* exported chartOptions */

var chartOptions = {
    cpu_usage: {
        chart: {
            renderTo: ''
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
            }
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
        series: [{
            name: '% CPU used',
            data: [],
            zones: [    // set zones color setting
                {
                    value: 10,
                    color: '#7cb5ec'
                },
                {
                    value: 80,
                    color: '#90ed7d'
                },
                {
                    value: 95,
                    color: 'orange'
                },
                {
                    color: 'red'
                }
            ]
        }]
    },
    loadavg: {
        chart: {
            renderTo: '',
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
            }
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
    },
    mem_usage: {
        chart: {
            renderTo: '',
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        legend: {
            enabled: false
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
    },
    inbound_traffic: {
        chart: {
            renderTo: ''
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        legend: {
            enabled: false
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
                text: 'Inbound'
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
    },
    outbound_traffic: {
        chart: {
            renderTo: ''
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        legend: {
            enabled: false
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
                text: 'Outbound'
            }
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
    },
    disks: {
        chart: {
            renderTo: '',
        },
        title: {
            text: ''
        },
        legend: {
            enabled: false
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
                text: 'Disk usage'
            },
            labels: {
                formatter: function () {
                   return Highcharts.numberFormat((this.value / 1024 / 1000), 0, '.', ',') + ' MB';
                }
            }
        },
        tooltip: {
            formatter: function () {
                return '<strong>' + Highcharts.numberFormat((this.y/1024/1000), 0, '.', ',') + ' MB '
                    + 'used</strong><br/>'
                    + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x*1000);
            }
        },
        series: [{
            name: 'DISKS',
            data: []
        }]
    }
}
