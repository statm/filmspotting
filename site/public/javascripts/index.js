$(document).ready(function() {
	initMap();
	initUI();
});

function initMap() {
	var mapOptions = {
		center : new google.maps.LatLng(37.09024, -95.712891),
		zoom : 5,
		noClear : true
	};
	var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
}

function initUI() {
	onResize();
	$(window).resize(onResize);
	$("#search-button").click(onSearch);
	$("#search-input").keypress(onSearchInput);
}

function onResize() {
	if (mapRevealed) {
	} else {
		$("#search-box").css("top", $(document).height() / 3);
	}
}

function onSearchInput() {
	if (mapRevealed) {
		return;
	}
	if ($("#search-input").val().length > 1) {
		revealMap();
	}
}

function onSearch() {
	// TODO
}

var mapRevealed = false;

function revealMap() {
	mapRevealed = true;
	var duration = 200;
	$("#search-box").animate({top: 50}, duration);
	$("#overlay").animate({opacity: 0}, duration).hide();
	$({blurRadius: 7}).animate({blurRadius: 0}, {
        duration: duration,
        step: function() {
            $('#map-canvas').css({
                "-webkit-filter": "blur("+this.blurRadius+"px)",
                "filter": "blur("+this.blurRadius+"px)"
            });
        }
    });
}