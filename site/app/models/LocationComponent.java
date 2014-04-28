package models;

import javax.persistence.Entity;

import play.db.jpa.Model;

@Entity
public class LocationComponent extends Model {
	
	public String shortName;
	public String longName;
	public String type;
	
}
