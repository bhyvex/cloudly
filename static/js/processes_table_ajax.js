/**
 * Pipelining function for DataTables. To be used to the `ajax` option of DataTables
 */
$.fn.dataTable.pipeline = function (opts) {
	// Configuration options
	var conf = $.extend({
		pages: 5,     	// number of pages to cache
		url: '',      	// script url
		headers: null,	// headers data
		data: null,		// function or object with parameters to send to the server
						// matching how `ajax.data` works in DataTables
		method: 'POST'	// Ajax HTTP method
	}, opts);

	// Private variables for storing the cache
	var cacheLower = -1;
	var cacheUpper = null;
	var cacheLastRequest = null;
	var cacheLastJson = null;

	return function (request, drawCallback, settings) {
		var ajax          = false;
		var requestStart  = request.start;
		var drawStart     = request.start;
		var requestLength = request.length;
		var requestEnd    = requestStart + requestLength;

		if (settings.clearCache) {
			// API requested that the cache be cleared
			ajax = true;
			settings.clearCache = false;
		} else if (cacheLower < 0 || requestStart < cacheLower || requestEnd > cacheUpper) {
			// outside cached data - need to make a request
			ajax = true;
		} else if (JSON.stringify(request.order) !== JSON.stringify(cacheLastRequest.order) ||
				JSON.stringify(request.columns) !== JSON.stringify(cacheLastRequest.columns) ||
				JSON.stringify(request.search) !== JSON.stringify(cacheLastRequest.search)
		) {
			// properties changed (ordering, columns, searching)
			ajax = true;
		}

		// Store the request for checking next time around
		cacheLastRequest = $.extend( true, {}, request );

		if (ajax) {
			// Need data from the server
			if (requestStart < cacheLower) {
				requestStart = requestStart - (requestLength*(conf.pages-1));

				if (requestStart < 0) {
					requestStart = 0;
				}
			}

			cacheLower = requestStart;
			cacheUpper = requestStart + (requestLength * conf.pages);

			request.start = requestStart;
			request.length = requestLength*conf.pages;

			// Provide the same `data` options as DataTables.
			if ($.isFunction(conf.data)) {
				// As a function it is executed with the data object as an arg
				// for manipulation. If an object is returned, it is used as the
				// data object to submit
				var d = conf.data(request);
				if (d) {
					$.extend(request, d);
				}
			} else if ($.isPlainObject(conf.data)) {
				// As an object, the data given extends the default
				$.extend(request, conf.data);
			}

			settings.jqXHR = $.ajax( {
				type: conf.method,
				url: conf.url,
				headers: conf.headers,
				data: request,
				dataType: "json",
				cache: false,
				success: function(json) {
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
					json.data = data;
					cacheLastJson = $.extend(true, {}, json);

					if (cacheLower != drawStart) {
						json.data.splice(0, drawStart-cacheLower);
					}
					json.data.splice(requestLength, json.data.length);

					drawCallback(json);
				}
			} );
		} else {
			json = $.extend(true, {}, cacheLastJson);
			json.draw = request.draw; // Update the echo for each response
			json.data.splice(0, requestStart-cacheLower);
			json.data.splice(requestLength, json.data.length);

			drawCallback(json);
		}
	}
};

// Register an API method that will empty the pipelined data, forcing an Ajax
// fetch on the next draw (i.e. `table.clearPipeline().draw()`)
$.fn.dataTable.Api.register('clearPipeline()', function () {
	return this.iterator('table', function (settings) {
		settings.clearCache = true;
	});
});

//
// DataTables initialisation
//
$(document).ready(function() {
	var server = $('input[name="hwaddr"]').val();
	var csrf = $('input[name="csrfmiddlewaretoken"]').val();
	var secret = $('input[name="secret"]').val();
	var address = '/ajax/server/' + server + '/metrics/processes/';

	$('#running_processes_table').dataTable({
		lengthMenu: [[15, 50, 100, -1], [15, 50, 100, "All"]],
		order: [[ 2, "desc" ]],
		processing: true,
		serverSide: true,
		ajax: $.fn.dataTable.pipeline({
			url: address,
			pages: 10, // number of pages to cache
			headers: {'X-CSRFToken': csrf},
			data: {
				secret: secret,
				server: server
			}
		})
	});
});
