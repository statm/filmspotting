package models;

import java.util.List;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.OneToMany;

import play.db.jpa.GenericModel;

@Entity
public class Movie extends GenericModel {
	@Id
	public Long id;
	public String imdbID;
	public String title;
	public String year;
	public String rate;
	public String genres;
	@Column(columnDefinition="TEXT")
	public String description;
	@Column(columnDefinition="TEXT")
	public String director;
	@Column(columnDefinition="TEXT")
	public String cast;
	@OneToMany
	public List<Location> locations;
}
