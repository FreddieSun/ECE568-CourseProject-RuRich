package org.ece568.FinalProject.model;

public class Comment {
	

	private String symbol;
	private String comment;
	private String timestamp;
	private String username;
	
	public Comment() {
		
	}
	
	public String getSymbol() {
		return symbol;
	}

	public void setSymbol(String symbol) {
		this.symbol = symbol;
	}

	public Comment(String symbol, String comment, String timestamp, String username) {
		this.symbol = symbol;
		this.comment = comment;
		this.timestamp = timestamp;
		this.username = username;
	}
	public String getComment() {
		return comment;
	}
	public void setComment(String comment) {
		this.comment = comment;
	}
	public String getTimestamp() {
		return timestamp;
	}
	public void setTimestamp(String timestamp) {
		this.timestamp = timestamp;
	}
	public String getUsername() {
		return username;
	}
	public void setUsername(String username) {
		this.username = username;
	}

	
}
