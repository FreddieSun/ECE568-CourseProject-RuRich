package org.ece568.FinalProject.model;

import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement
public class DailyStock {

//    private String id;
    private BigDecimal open;
    private BigDecimal high;
    private BigDecimal low;
    private BigDecimal close;
    private int volume;
    private String timeStamp;
    private String symbol;
    
    public DailyStock() {
    	
    }

    public DailyStock(String symbol, BigDecimal open, BigDecimal high, BigDecimal low, BigDecimal close, int volume, String timeStamp) {
        this.symbol = symbol;
//        this.id = id;
        this.open = open;
        this.high = high;
        this.low = low;
        this.close = close;
        this.volume = volume;
        this.timeStamp = timeStamp;
    }

    public void setSymbol(String symbol) {
        this.symbol = symbol;
    }

//    public void setId(String id) {
//        this.id = id;
//    }

    public void setOpen(BigDecimal open) {
        this.open = open;
    }

    public void setHigh(BigDecimal high) {
        this.high = high;
    }

    public void setLow(BigDecimal low) {
        this.low = low;
    }

    public void setClose(BigDecimal close) {
        this.close = close;
    }

    public void setVolume(int volume) {
        this.volume = volume;
    }

    public void setTimeStamp(String timeStamp) {
        this.timeStamp = timeStamp;
    }

    public BigDecimal getOpen() {
        return open;
    }

    public BigDecimal getHigh() {
        return high;
    }

    public BigDecimal getLow() {
        return low;
    }

    public BigDecimal getClose() {
        return close;
    }




    public String getTimeStamp() {
        return timeStamp;
    }

    public String getSymbol() {
        return symbol;
    }

//    public String getId() {
//        return id;
//    }

    public int getVolume() {
        return volume;
    }



}
