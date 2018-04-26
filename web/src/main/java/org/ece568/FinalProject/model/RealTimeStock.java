package org.ece568.FinalProject.model;

import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlRootElement;


@XmlRootElement
public class RealTimeStock {
	private String symbol;
	private String timeStamp;
    private int volume;
    private BigDecimal price;
    
    public RealTimeStock() {
    
    }
    
    public RealTimeStock(String symbol, BigDecimal price) {
    	this.symbol = symbol;
    	this.price = price;
    }
    
    public RealTimeStock(String symbol, String timeStamp, int volume, BigDecimal price) {
    	this.price = price;
    	this.timeStamp = timeStamp;
    	this.symbol = symbol;
    	this.volume = volume;
    }
    
	public String getSymbol() {
		return symbol;
	}
	public void setSymbol(String symbol) {
		this.symbol = symbol;
	}
	public String getTimeStamp() {
		return timeStamp;
	}
	public void setTimeStamp(String timeStamp) {
		this.timeStamp = timeStamp;
	}
	public int getVolume() {
		return volume;
	}
	public void setVolume(int volume) {
		this.volume = volume;
	}
	public BigDecimal getPrice() {
		return price;
	}
	public void setPrice(BigDecimal price) {
		this.price = price;
	}
    
    
}
