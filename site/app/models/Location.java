package models;

import javax.persistence.Column;
import javax.persistence.Entity;

import play.db.jpa.Model;

@Entity
public class Location extends Model {
	public Long movieID;
	@Column(columnDefinition="TEXT")
	public String movieLocation;
	@Column(columnDefinition="TEXT")
	public String actualLocation;
	@Column(columnDefinition="TEXT")
	public String formattedAddress;
	@Column(columnDefinition="TEXT")
	public String addressComponents;
	public Double latitude;
	public Double longitude;
	public String source;
}
