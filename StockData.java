/** 
 * 股票实体类 
 * @ 2013.01.02 
 */  
public class StockData {  
	
	public String getDate() {
		return date;
	}
	public void setDate(String date) {
		this.date = date;
	}
	public double getOpen() {
		return open;
	}
	public void setOpen(double open) {
		this.open = open;
	}
	public double getHigh() {
		return high;
	}
	public void setHigh(double high) {
		this.high = high;
	}
	public double getLow() {
		return low;
	}
	public void setLow(double low) {
		this.low = low;
	}
	public double getClose() {
		return close;
	}
	public void setClose(double close) {
		this.close = close;
	}
	public double getAdjusted_close() {
		return adjusted_close;
	}
	public void setAdjusted_close(double adjusted_close) {
		this.adjusted_close = adjusted_close;
	}
	public double getVolume() {
		return volume;
	}
	public void setVolume(double volume) {
		this.volume = volume;
	}
	private String date; // 交易日期  
    private double open = 0.0; // 开盘价  
    private double high = 0.0; // 最高价  
    private double low = 0.0; // 最低价  
    private double close = 0.0; // 最后一次交易价格，相当于收盘价  
    private double adjusted_close = 0.0; // 最后一次交易价格 (今天的收盘价当做加权价格)   
    private double volume = 0.0;// 总交易手  
    //setters and getters.....省略  
    //toString method...为测试方便可以加个toString方法，省略  
} 
