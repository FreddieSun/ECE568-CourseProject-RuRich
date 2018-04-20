package org.ece568.FinalProject.service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

import javax.ws.rs.core.Response;

import org.ece568.FinalProject.databaseUtil.DBUtil;
import org.ece568.FinalProject.model.*;
import org.json.JSONObject;

public class StockService {
	DBUtil dbUtil = new DBUtil();
	
	/*
	 * 4.1 1. Show the list of all companies in the database 
	 * along with their latest stock price (real time latest stock price)
	 */

	public List<RealTimeStock> getAllStock() {
		return dbUtil.getAllStock();
	}
	
	/*
	 * 4.2 Get the highest stock price of any company in the last ten days
	 * 
	 */
	public Response getMax(String symbol) {
		return dbUtil.getMax(symbol);
		
	}
	
	/*
	 * 4.3 Average stock price of any company in the latest one year.
	 */
	public Response getAvg(String symbol) {
		return dbUtil.getAvg(symbol);
		
	}
	/*
	 * 4.4 Lowest stock price for any company in the latest one year.
	 */
	public Response getMin(String symbol) {
		return dbUtil.getMin(symbol);
		
	}
	
	
	/*
	 * 4.5 List the ids of companies along with their name who have the average stock price 
	 * lesser than the lowest of any of the Selected Company in the latest one year
	 */
	
	public List<Integer> getAllSpecificStockId() {
		List<Integer> list = new ArrayList<>();
		return list;
	}
	

	
	public Response getDay(String symbol) {
		return dbUtil.getDay(symbol);
	}
	
	public Response getMonth(String symbol) {
		return dbUtil.getMonth(symbol);
	}
	
	public Response getYear(String symbol) {
		return dbUtil.getYear(symbol);
	}
	
	public Response addComment(String symbol, String comment, String timestamp, String username) {
		return dbUtil.addComment(symbol, comment, timestamp,  username);
	}
	
	public Response getComment(String symbol) {
		return dbUtil.getComment(symbol);
	}

}
