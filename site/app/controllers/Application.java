package controllers;

import play.*;
import play.mvc.*;

import java.util.*;

import models.*;

public class Application extends Controller {

    public static void index() {
        render();
    }
    
    public static void search(String query) {
    	List<Object[]> movieResults = Movie.find("select m.id, m.imdbID, m.title, m.year from Movie m where m.title like '%" + query + "%'").fetch();
    	
    	SearchResult searchResult = new SearchResult(movieResults);
    	renderJSON(searchResult);
    }
    
    public static void showMovie(Long id) {
    	renderJSON(Movie.findById(id));
    }
    
    public static class SearchResult {
    	List<MovieResult> movies = new ArrayList<MovieResult>();
    	
    	public SearchResult(List<Object[]> movieResults) {
    		for (Object[] entry : movieResults) {
    			this.movies.add(new MovieResult(entry));
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
}

