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
            setTimeout(onTypeAhead, 500);
            return;
		}
        
        onTypeAhead();
	}
    
    function onTypeAhead() {
        var inputText = $("#search-input").val();
        if (inputText.length < 2) {
            return;
        }
        
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
		var duration = 300;
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
		$("#search-box").animate({"margin-left": 400, left: 70, right: 70}, {duration : duration, queue : false});
        
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
        
        clearMarkers();
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
    var markers = [];
    var infoWindow;
    
    function initMap() {
        var mapOptions = {
            center : new google.maps.LatLng(40, -75),
            zoom : 4,
            noClear : true,
            disableDefaultUI : true
        };
        map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
    }
    
    function clearMarkers() {
        for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(null);
        }
        markers = [];
    }
    
    function addMarkers(locations) {
        for (var i = 0; i < locations.length; i ++) {
            var address = locations[i].actual_location;
            var geocodingURL = "https://maps.googleapis.com/maps/api/geocode/json?address=" + encodeURIComponent(address) + "&sensor=false";
            (function(i, locationInfo) {
                $.getJSON(geocodingURL,
                      function(data) {
                          if (data.status == "OK"
                             && data.results.length > 0) {
                              
                              var location = data.results[0].geometry.location;
                              
                              var marker = new google.maps.Marker({
                                  position: new google.maps.LatLng(location.lat, location.lng),
                                  map: map,
                                  title: location.actual_location,
                                  animation: google.maps.Animation.DROP
                              });
                              markers[i] = marker;
                              
                              $(".location-entry").slice(i, i + 1).click(function() {
                                  panTo(marker);
                                  bounceMarker(marker);
                                  // showStreetView(marker);
                                  
                              });
                              
                              google.maps.event.addListener(marker, "click", function() {
                                  if (infoWindow) {
                                      infoWindow.close();
                                  }
                                  infoWindow = new google.maps.InfoWindow({
                                      maxWidth: 400,
                                      content: Mustache.to_html($("#marker-window-tmpl").text(), locationInfo)
                                  });
                                  infoWindow.open(map, marker);
                              });
                          } else {
                              console.log("geocoding failed for address: " + address);
                          }
                      });
            })(i, locations[i]);
        }
    }

    function panTo(marker) {
        map.panTo(marker.getPosition());
    }

    function bounceMarker(marker) {
        marker.setAnimation(google.maps.Animation.BOUNCE);
        setTimeout(function () {
            marker.setAnimation(null);
        }, 1400);
    }


    // ======================================
    //  Street View Control
    // ======================================
    
    function showStreetView(marker) {
        var panorama = map.getStreetView();
        panorama.setPosition(marker.getPosition());
        panorama.setVisible(true);
    }
    
})(document);