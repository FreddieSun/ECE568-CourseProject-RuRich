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
	
	public Response getDataForFigure(String symbol) {
		return dbUtil.getDataForFigure(symbol);
		
	}
}
