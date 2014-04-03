$(document).ready(function() {
	initMap();
	initUI();
//	revealMap();
});

function initMap() {
	var mapOptions = {
		center : new google.maps.LatLng(37.09024, -95.712891),
		zoom : 5,
		noClear : true,
		disableDefaultUI : true
	};
	var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
}

function initUI() {
	onResize();
	$(window).resize(onResize);
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
	
	revealMap();
	showInfoBox();
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

function showInfoBox() {
	var duration = 200;
	$("#map-canvas").animate({left: 300}, duration);
	$("#info-box").animate({width: 300}, duration);
}