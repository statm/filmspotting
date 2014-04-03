(function(document) {
	$(document).ready(function() {
		initMap();
		initUI();
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
	
	function onSearchInput(event) {
		if (!mapRevealed) {
			revealMap();
			showSearchSuggestion();
		}
		
		if (event.keyCode == 13) { // Enter pressed
			// TODO
		}
	}
	
	var mapRevealed = false;
	
	function revealMap() {
		mapRevealed = true;
		var duration = 200;
		$("#search-box").animate({top: 40}, {duration : duration, queue : false});
		$("#overlay").animate({opacity: 0}, {duration : duration, queue : false}).hide();
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
		$("#map-canvas").animate({left: 400}, {duration : duration, queue : false});
		$("#info-box").animate({width: 400}, {duration : duration, queue : false});
		$("#search-box").animate({"margin-left": 400, left: 80, right: 80}, {duration : duration, queue : false});
	}
	
	function hideInfoBox() {
		var duration = 200;
		$("#map-canvas").animate({left: 0}, {duration : duration, queue : false});
		$("#info-box").animate({width: 0}, {duration : duration, queue : false});
		$("#search-box").animate({"margin-left": 0, left: 200, right: 200}, {duration : duration, queue : false});
	}
	
	function showSearchSuggestion() {
		$("#search-suggestion").show();
	}
	
	function hideSearchSuggestion() {
		$("#search-suggestion").hide();
	}
})(document);