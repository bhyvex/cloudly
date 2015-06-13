$(function () {
	$(document).ready(function () {
		var server = $('input[name="hwaddr"]').val();
		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
		var secret = $('input[name="secret"]').val();

		cpu_usage_set(csrf, server, secret);
		processes(csrf, server, secret);
//		loadavg_set (csrf, server, secret);
	});
});

function processes(csrf, server, secret) {
	var address = '/ajax/server/' + server + '/metrics/processes/';

	$('#running_processes_table').dataTable({
		lengthMenu: [[15, 50, 100], [15, 50, 100]],
		order: [[ 2, "desc" ]],
		draw: 1,
		processing: true,
		serverSide: true,
		ajax: {
			url: address,
			type: 'POST',
			dataType: 'json',
			dataSrc: function(json) {
				var data = [];
				for (var i = 0; i < json.data.length; i++) {

					var user = '';
					if (json.data[i]['cpu']  > 50) {
						user += '<span class="label label-danger">';
					} else {
						user += '<span class="label label-success">';
					}
					user += json.data[i]['user'];
					user += '</span>';

					data.push([
						json.data[i]['pid'],
						user,
						json.data[i]['cpu'],
						json.data[i]['mem'],
						json.data[i]['command'][0]
							.replace('[','')
							.replace(']',''),
						json.data[i]['command'].join(' ')
							.replace('[','')
							.replace(']','')
					]);
				}
				console.log(data);
				return data;
			},
			headers: {
				'X-CSRFToken': csrf
			},
			cache: false,
			data: {
				'server': server,
				'secret': secret
			}
		}
	}); //dataTable function end
}

function cpu_usage_set (csrf, server, secret) {
	var address = '/ajax/server/' + server + '/metrics/cpu_usage/';
	var lastValue = null;

	function requestCpuUsageData(series, lastValue, csrf, server, secret) {
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
				'lastvalue': lastValue
			},
			success: function(data) {
				if (typeof element === 'undefined') {
					var element = [null, null];
				}

				if (data[0] != element[0]) {
					series.addPoint(data[0], true, true);
					element[0] = data[0];
				}
			},
			error: function(data, textStatus, errorThrown) {
				console.log('error: ' + textStatus);
				console.log('error: ' + errorThrown);
			}
		});
	}

	function updateCpuUsageChart(series, lastValue, csrf, server, secret) {
		setInterval(function() {
			requestCpuUsageData(series, lastValue, csrf, server, secret);
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
			'X-CSRFToken': csrf
		},
		cache: false,
		data: {
			'server': server,
			'secret': secret,
			'lastvalue': lastValue
		},
		success: function(data) {
			console.log('naplneni daty');
			if (data != null) {
				var optionalData = [];
				var optionalLength = 30;
				console.log(data);
				var dataLength = data.length;
				data.reverse();
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
									data[0][0],
									csrf,
									server,
									secret
								);
							}
						}
					},
					title: {
						text: 'CPU Usage'
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
						data: optionalData,
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
			tickPixelInterval: 1000
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
