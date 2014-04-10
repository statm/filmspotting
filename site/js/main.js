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
        $("#search-input").on("keydown", null, null, onSearchKeyPress);
        $("#search-input").focus();
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
            return;
		}
        
        onTypeAhead();
	}
    
    function onSearchKeyPress(event) {
        if (event.keyCode == 38) { // up
            selectedIndex -= 1;
            if (selectedIndex < 0) {
                selectedIndex = 0;
            }
            applySelectedIndex();
            event.preventDefault();
        } else if (event.keyCode == 40) { // down
            selectedIndex += 1;
            if (selectedIndex >= $(".suggestion-item").length) {
                selectedIndex = $(".suggestion-item").length - 1;
            }
            applySelectedIndex();
            event.preventDefault();
        } else if (event.keyCode == 13) { // enter
            onSelectMovie();
        }
    }
    
    var suggestionData;
    
    function onTypeAhead() {
        var inputText = $("#search-input").val();
        if (inputText.length < 2) {
            return;
        }
        
        var suggestions = getSuggestion(inputText);
        
        if (suggestions.length > 0) {
            suggestionData = {data: suggestions};
            showSearchSuggestion();
        } else {
            suggestionData = {};
            hideSearchSuggestion();
        }
    }

	var mapRevealed = false;

	function revealMap() {
        mapRevealed = true;
		var duration = 400;
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
    
    var lastMouseX, lastMouseY;

	function showSearchSuggestion() {
        $("#search-input").addClass("search-input-with-suggestion");
        
        var suggestionPanel = $("#search-suggestion");
		suggestionPanel.show();
        suggestionPanel.empty();
        
        var suggestionTmpl = $("#suggestion-tmpl").text();
        suggestionPanel.html(Mustache.to_html(suggestionTmpl, suggestionData));
        
        $(".suggestion-item").each(function(index) {
            $(this).click(function() {
                if (selectedIndex != index) {
                    selectedIndex = index;
                    applySelectedIndex();
                }
                
                onSelectMovie();
            });
            $(this).mousemove(function(event) {
                if (event.pageX == lastMouseX
                    && event.pageY == lastMouseY) {
                    return;
                }
                
                lastMouseX = event.pageX;
                lastMouseY = event.pageY;
                
                if (selectedIndex != index) {
                    selectedIndex = index;
                    applySelectedIndex();
                }
            });
        });
        
        applySelectedIndex();
	}

	function hideSearchSuggestion() {
        $("#search-input").removeClass("search-input-with-suggestion");
		$("#search-suggestion").hide();
	}
    
    function onSelectMovie() {
        var movieData = suggestionData.data[selectedIndex]
        
        $("#search-input").val(movieData.name);
        hideSearchSuggestion();
        
        showInfoBox(movieData);
        
        clearMarkers();
        addMarkers(movieData.locations);
        
        $("#search-input").blur();
    }
    
    var selectedIndex = 0;
    
    function applySelectedIndex() {
        var selectedElement;
        
        $(".suggestion-item").each(function(index) {
            if (index == selectedIndex) {
                $(this).addClass("search-suggestion-active");
                selectedElement = $(this);
            } else {
                $(this).removeClass("search-suggestion-active");
            }
        });
        
        // ensure element visible
        var container = $("#search-suggestion");
        
        var topDelta = selectedElement.offset().top - container.offset().top;
        if (topDelta < 0) {
            container.animate({"scrollTop" : container.scrollTop() + topDelta},
                              {duration: 40, 
                               queue: false
                              });
        }
        
        var bottomDelta = selectedElement.offset().top + selectedElement.height()
                        - container.offset().top - container.height() - 16;
        if (bottomDelta > 0) {
            container.animate({"scrollTop" : container.scrollTop() + bottomDelta},
                              {duration: 40, 
                               queue: false
                              });
        }
    }
    
    
    // ======================================
    //  Data
    // ======================================
    
    var data;

    function loadData() {
        $.ajax({
            type: "GET",
            url: "data/link.json",
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
            disableDefaultUI : true,
            mapTypeId: google.maps.MapTypeId.HYBRID
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
                                  
                                  panTo(marker);
                              });
                          } else {
                              console.log("geocoding failed for address: " + locationInfo.actual_location);
                          }
                      });
            })(i, locations[i]);
        }
    }

    function panTo(marker) {
        map.panTo(marker.getPosition());
        map.setZoom(21);
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