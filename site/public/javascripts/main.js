//(function(document) {
    "use strict";
    
	$(document).ready(function() {
		initMap();
		initUI();
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
        	if (selectedIndex < suggestionData.movies.length) {
            	selectMovie(suggestionData.movies[selectedIndex]);
            } else {
            	selectLocation(suggestionData.locations[selectedIndex - suggestionData.movies.length]);
            }
        }
    }
    
    var suggestionData;
    
    function onTypeAhead() {
        var inputText = $("#search-input").val();
        if (inputText.length < 2) {
            return;
        }
        
        $.getJSON("/search/" + inputText, function(data) {
        	if (data.movies.length > 0 || data.locations.length > 0) {
	        	suggestionData = data;
	        	showSearchSuggestion();
        	} else {
        		suggestionData = {};
        		hideSearchSuggestion();
        	}
        })
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

	function showInfoBoxWithMovieData(movieData) {
		var duration = 200;
		$("#map-canvas").animate({left: 400}, {duration : duration, queue : false});
		$("#info-box").animate({width: 400}, {duration : duration, queue : false});
		$("#search-box").animate({"margin-left": 400, left: 70, right: 70}, {duration : duration, queue : false});
        
        var infoBox = $("#info-box");
        infoBox.empty();
        
        movieData.genres = eval(movieData.genres);
        if (movieData.genres != null) {
        	movieData.genres = movieData.genres.join(" / ")
        }
        movieData.director = eval(movieData.director);
        movieData.cast = eval(movieData.cast);
        
        var infoBoxTmpl = $("#info-box-movie-tmpl").text();
        infoBox.html(Mustache.to_html(infoBoxTmpl, movieData));
	}
	
	function showInfoBoxWithLocationData(locationData, movies) {
		var duration = 200;
		$("#map-canvas").animate({left: 400}, {duration : duration, queue : false});
		$("#info-box").animate({width: 400}, {duration : duration, queue : false});
		$("#search-box").animate({"margin-left": 400, left: 70, right: 70}, {duration : duration, queue : false});
		
        var infoBox = $("#info-box");
        infoBox.empty();
        
        var infoBoxTmpl = $("#info-box-location-tmpl").text();
        infoBox.html(Mustache.to_html(infoBoxTmpl, {location: locationData, movies: movies, movieCount: movies.length}));
        (function(movies) {
	        $(".location-movie-entry").each(function(index) {
	            $(this).click(function() {
	                selectMovie(movies[index]);
	            });
	        });
        })(movies);
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
                
                if (index < suggestionData.movies.length) {
                	selectMovie(suggestionData.movies[selectedIndex]);
                } else {
                	selectLocation(suggestionData.locations[selectedIndex - suggestionData.movies.length]);
                }
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
    
    function selectMovie(movie) {
    	var movieID = movie.id;
    	$("#search-input").val(movie.title);
    	hideSearchSuggestion();
    	$("#search-input").blur();
    	
    	$.getJSON("/movie/" + movieID, function(data) {
    		showInfoBoxWithMovieData(data);
    		
    		clearMarkers();
    		addMarkers(data.locations);
    	});
    }
    
    function selectLocation(location) {
    	var locationID = location.id;
    	
    	$("#search-input").val(location.shortName);
    	hideSearchSuggestion();
    	$("#search-input").blur();
    	
    	$.getJSON("/location/" + locationID, function(data) {
    		showInfoBoxWithLocationData(location, data);
    		clearMarkers();
    	});
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
            if (markers[i] != undefined) {
                markers[i].setMap(null);
            }
        }
        markers = [];
    }
    
    function addMarkers(locations) {
        for (var i = 0; i < locations.length; i ++) {
            var address = locations[i].actualLocation;
            
            (function(i, location) {
                if (location.latitude != null
                	&& location.longitude != null) {
                	
                    var marker = new google.maps.Marker({
                                      position: new google.maps.LatLng(location.latitude, location.longitude),
                                      map: map,
                                      title: location.actualLocation,
                                      animation: google.maps.Animation.DROP
                                  });
                    markers[i] = marker;

                    $(".location-entry").slice(i, i + 1).click(function() {
                        panTo(marker);
                        bounceMarker(marker);
                        showInfoWindow(location, marker);
                    });

                    google.maps.event.addListener(marker, "click", function() {
                        showInfoWindow(location, marker);
                    });
                
                } else {
                    console.log("geocoding failed for address: " + locations[i].actualLocation);
                }
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
    
    function showInfoWindow(locationInfo, marker) {
        if (infoWindow) {
            infoWindow.close();
        }
        infoWindow = new google.maps.InfoWindow({
            maxWidth: 400,
            content: Mustache.to_html($("#marker-window-tmpl").text(), locationInfo)
        });
        infoWindow.open(map, marker);

        panTo(marker);
    }


    // ======================================
    //  Street View Control
    // ======================================
    
    function showStreetView(marker) {
        var panorama = map.getStreetView();
        panorama.setPosition(marker.getPosition());
        panorama.setVisible(true);
    }
    
//})(document);