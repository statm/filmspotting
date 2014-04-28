package controllers;

import play.*;
import play.db.jpa.JPA;
import play.mvc.*;

import java.util.*;

import javax.persistence.Query;

import models.*;

public class Application extends Controller {

    public static void index() {
        render();
    }
    
    public static void search(String query) {
    	List<Object[]> movieResults = Movie.find("select m.id, m.imdbID, m.title, m.year from Movie m where m.title like '%" + query + "%' order by m.rate desc").fetch();
    	List<LocationComponent> locationResults = LocationComponent.find("from LocationComponent lc where lc.shortName like '%" + query + "%' or lc.longName like '%" + query + "%'").fetch();
    	
    	SearchResult searchResult = new SearchResult(movieResults, locationResults);
    	renderJSON(searchResult);
    }
    
    public static void showMovie(Long id) {
    	renderJSON(Movie.findById(id));
    }
    
    public static void showLocation(Long id) {
    	LocationComponent component = LocationComponent.findById(id);
    	
    	List<Object[]> movies = Movie.find("select distinct m.id, m.imdbID, m.title, m.year from Movie m, Location l where l.addressComponents like '%" + component.longName + "%' and l.movieID=m.id order by m.rate desc").fetch();
    	ArrayList<MovieResult> result = new ArrayList<MovieResult>();
    	for (Object[] entry : movies) {
    		result.add(new MovieResult(entry));
    	}
    	renderJSON(result);
    }
    
    public static class SearchResult {
    	List<MovieResult> movies;
    	List<LocationComponent> locations;
    	
    	public SearchResult(List<Object[]> movieResults, List<LocationComponent> locationResults) {
    		movies = new ArrayList<MovieResult>();
    		for (Object[] entry : movieResults) {
    			this.movies.add(new MovieResult(entry));
    		}
    		
    		this.locations = locationResults;
    	}
    }
    
    public static class MovieResult {
		public Long id;
		public String imdbID;
    	public String title;
    	public String year;
    	
    	public MovieResult(Object[] entry) {
    		this.id = (Long)(entry[0]);
    		this.imdbID = (String)(entry[1]);
    		this.title = (String)(entry[2]);
    		this.year = (String)(entry[3]);
    	}
    }
}

