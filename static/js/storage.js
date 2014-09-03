function ajaxStorage() {
	$.ajax({ url: "/ajax/cloud/storage/", type: "GET", dataType: "html", success: ajaxStorageUpdate });
}

function ajaxStorageUpdate(content) {
	$('#storage_datatable').html(content);
	// prevent moving to top
	$('a[href="#"][data-top!=true]').click(function(e){ e.preventDefault(); });

}

function thumbnailCheck(zone, file, ext, path) {
	var fExt = file.name.toLowerCase().substring(file.name.length - ext.length);
	if (fExt != ext) return false;
	zone.emit("thumbnail", file, path);
	return true;
}

function setupDropzone(zone) {
	if (zone == undefined) return;
	zone.on("addedfile", function(file) {
		// images already handled
		if (file.type.match(/image.*/)) return;
		// Okey, sem treba rovnako pridat dalsie typy. file.type je MIME, file.name je nazov
		if (thumbnailCheck(zone, file, ".txt", "/static/images/icon-todo.png")) return;
		if (thumbnailCheck(zone, file, ".wav", "/static/images/icon-todo.png")) return;
	});
}

$(document).ready (function() {
	window.setInterval ( function() { ajaxStorage(); } , 2000);

	window.setTimeout( function() { setupDropzone(Dropzone.instances[0]); }, 500);
});

