
function setupDropzone(zone) {
	if (zone == undefined) return;
	zone.on("addedfile", function(file) {
		// images already handled
		if (file.type.match(/image.*/)) return;
		// Okey, sem treba rovnako pridat dalsie typy. file.type je MIME, file.name je nazov
		if (file.type == 'text/plain') {
			zone.emit("thumbnail", file, "/static/images/jan-avatar.png");  // obrazok samozrejme treba zmenit
			return;
		}
		if (file.type == 'audio/mpeg') {
			zone.emit("thumbnail", file, "/static/images/jan-avatar.png");  // obrazok samozrejme treba zmenit
			return;
		}

	});
}

$(document).ready (function() {

	window.setTimeout( function() { setupDropzone(Dropzone.instances[0]); }, 500);
});


