/**
 * CPU Usage
 *
 * Set all action for CPU Usage chart
 * (code standards: http://javascript.crockford.com/code.html)
 */

/**
 * Set duration by interval value
 */
function setChartDuration(interval) {
    var duration = '3000';      // base duration value
    if (interval == '15m') {
        duration = '15000';
    } else if (interval == '1h') {
        duration = '60000';
    } else if (interval == '1d') {
        duration = '300000';
    } else if (interval == '7d') {
        duration = '1800000';
    } else if (interval == '30d') {
        duration = '43200000';
    } else if (interval == 'at') {
        duration = '1800000';
    }
    return duration;
}

/**
 * Get new data via ajax call and set it to given serie
 */
function requestNewChartData(address, chart, interval, updateChart, mountPoint) {
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
            'mountPoint': mountPoint
        },
        success: function(data) {
            if (data !== undefined && data !== null && data[0].length > 0) {
                for (var i = 0; i < data.length; i++) {
                    chart.series[i].setData(data[0].reverse(), true, true, true); // add data set to chart serie
                }
            }
        },
        error: function(data, textStatus, errorThrown) {
            console.log('error: ' + textStatus);
            console.log('error: ' + errorThrown);
        }
    });
}
                    
var disks = $('input[name="available_disks_graphs"]').val();

    disks = disks
        .replace(']', '')
        .replace('[', '')
        .replace(/"/g, '')
        .split(','); 

for (i = 0; i < disks.length; i++) {

    var templateMountPoint = disks[i].replace(/\//g, 'slash');

    var temp = {
        'mountPoint': disks[i],
        'intervalName' : templateMountPoint + 'Interval',
        'chart': new Highcharts.Chart({  // create chart object
            chart: {
                renderTo: templateMountPoint + '_chart_id',
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
                    text: 'Disk usage'
                },
                labels: {
                    formatter: function () {
                       return Highcharts.numberFormat((this.value / 1024 / 1000), 0, '.', ',') + ' MB';
                    } 
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function () {
                    return '<strong>' + Highcharts.numberFormat((this.y/1024/1000), 0, '.', ',') + ' MB '
                        + 'used</strong><br/>'
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
                name: 'DISKS',
                data: []
            }]
        })
    }

    requestNewChartData(
        addressDisks,
        temp.chart,
        interval,
        true,
        temp['mountPoint']
    );
}
