(function(document) {
    "use strict";
    
	$(document).ready(function() {
		initMap();
		initUI();
        loadData();
	});
    
    
    // ======================================
    //  UI Control
    // ======================================
    
	function initUI() {
		onResize();
		$(window).resize(onResize);
		$("#search-input").on("input", null, null, onSearchInput);
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
		}
        
        var inputText = $("#search-input").val();
        var suggestions = getSuggestion(inputText);
        if (suggestions.length > 0) {
            showSearchSuggestion({data: suggestions});
        } else {
            hideSearchSuggestion();
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

	function showInfoBox(movieData) {
		var duration = 200;
		$("#map-canvas").animate({left: 400}, {duration : duration, queue : false});
		$("#info-box").animate({width: 400}, {duration : duration, queue : false});
		$("#search-box").animate({"margin-left": 400, left: 80, right: 80}, {duration : duration, queue : false});
        
        var infoBox = $("#info-box");
        infoBox.empty();
        
        var infoBoxTmpl = $("#info-box-tmpl").text();
        infoBox.html(Mustache.to_html(infoBoxTmpl, movieData));
	}

	function hideInfoBox() {
		var duration = 200;
		$("#map-canvas").animate({left: 0}, {duration : duration, queue : false});
		$("#info-box").animate({width: 0}, {duration : duration, queue : false});
		$("#search-box").animate({"margin-left": 0, left: 200, right: 200}, {duration : duration, queue : false});
	}

	function showSearchSuggestion(suggestionData) {
        $("#search-input").addClass("search-input-with-suggestion");
        
        var suggestionPanel = $("#search-suggestion");
		suggestionPanel.show();
        suggestionPanel.empty();
        
        var suggestionTmpl = $("#suggestion-tmpl").text();
        suggestionPanel.html(Mustache.to_html(suggestionTmpl, suggestionData));
        
        $(".suggestion-item").each(function(index) {
            $(this).click(function() {
                onSelectMovie(suggestionData.data[index]);
            });
        });
	}

	function hideSearchSuggestion() {
        $("#search-input").removeClass("search-input-with-suggestion");
		$("#search-suggestion").hide();
	}
    
    function onSelectMovie(movieData) {
        $("#search-input").val(movieData.name);
        hideSearchSuggestion();
        showInfoBox(movieData);
        addMarkers(movieData.locations);
    }
    
    
    // ======================================
    //  Data
    // ======================================
    
    var data;

    function loadData() {
        $.ajax({
            type: "GET",
            url: "data/imdb_data.json",
            success: function(result) {
                data = result;
            },
            async: false
        });
    }
    
    function getSuggestion(input) {
        var result = [];
        
        for (var i = 0; i < data.length; i ++) {
            if (data[i].name.toLowerCase().indexOf(input.toLowerCase()) != -1) {
                result.push(data[i]);
            }
        }
        
        return result;
    }
    
    
    // ======================================
    //  Map Control
    // ======================================
    
    var map;
    
    function initMap() {
        var mapOptions = {
            center : new google.maps.LatLng(37.09024, -95.712891),
            zoom : 5,
            noClear : true,
            disableDefaultUI : true
        };
        map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
    }
    
    function clearMarkers() {
    }
    
    function addMarkers(locations) {
        for (var i = 0; i < locations.length; i ++) {
            var address = locations[i].actual_location;
            var geocodingURL = "https://maps.googleapis.com/maps/api/geocode/json?address=" + encodeURIComponent(address) + "&sensor=false";
            $.getJSON(geocodingURL,
                      function(data) {
                          if (data.status == "OK"
                             && data.results.length > 0) {
                              var location = data.results[0].geometry.location;
                              var marker = new google.maps.Marker({
                                  position: new google.maps.LatLng(location.lat, location.lng),
                                  map: map});
                          } else {
                              console.log("geocoding failed for address: " + address);
                          }
                      });
        }
        
    }
    
})(document);