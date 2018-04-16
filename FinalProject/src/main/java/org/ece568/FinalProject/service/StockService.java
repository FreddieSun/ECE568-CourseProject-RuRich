package org.ece568.FinalProject.service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

import org.ece568.FinalProject.databaseUtil.DBUtil;
import org.ece568.FinalProject.model.*;

public class StockService {
	DBUtil dbUtil = new DBUtil();
	/*
	 * 4.1 1. Show the list of all companies in the database 
	 * along with their latest stock price (real time latest stock price)
	 */

	public List<RealTimeStock> getAllStock() {
//		BigDecimal price1 = new BigDecimal("26.00");
//		BigDecimal price2 = new BigDecimal("26.01");
//
//		RealTimeStock stock1 = new RealTimeStock("Google", "2018-04-16T01:22:43.091503+00:00 ", 12, price1);
//		RealTimeStock stock2 = new RealTimeStock("Apple", "2018-04-16T01:22:44.091503+00:00 ", 13, price2);

//		List<RealTimeStock> list = new ArrayList<>();
//		list.add(stock1);
//		list.add(stock2);
		
//		
		return dbUtil.getAllStock();
	}
	
	
	/*
	 * 4.2 Get the highest stock price of any company in the last ten days
	 * 
	 */
	public BigDecimal getHighestPrice(String symbol) {
		BigDecimal res = new BigDecimal("");
		return res;
	}
	
	/*
	 * 4.3 Average stock price of any company in the latest one year.
	 */
	public BigDecimal getAvgPrice(String symbol) {
		BigDecimal res = new BigDecimal("");
		return res;
	}
	
	/*
	 * 4.4 Lowest stock price for any company in the latest one year.
	 */
	public BigDecimal getLowestPrice(String symbol) {
		BigDecimal res = new BigDecimal("");
		return res;
	}
	
	/*
	 * 4.5 List the ids of companies along with their name who have the average stock price 
	 * lesser than the lowest of any of the Selected Company in the latest one year
	 */
	
	public List<Integer> getAllSpecificStockId() {
		List<Integer> list = new ArrayList<>();
		return list;
	}
}
