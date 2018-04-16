package org.ece568.FinalProject.databaseUtil;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;


import org.ece568.FinalProject.model.RealTimeStock;

import com.mongodb.Block;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import static com.mongodb.client.model.Filters.*;
import com.mongodb.client.model.Sorts;


import org.bson.Document;


public class DBUtil {
	public final String[] STOCK_LIST = {"GOOG", "AABA", "FB", "MSFT", "TWTR", "AAPL", "JPM", "AMZN", "JNJ", "BNC"};
    public static final String URL = "mongodb://ece568:ece568project@zwithc.cn:27017";

	/*
	 * 4.1 1. Show the list of all companies in the database 
	 * along with their latest stock price (real time latest stock price)
	 */
	public List<RealTimeStock> getAllStock() {
		final List<RealTimeStock> list = new ArrayList<>();
        MongoClient mongoClient = new MongoClient(new MongoClientURI(URL));

        // connecting to mongodb
        MongoDatabase mongoDatabase = mongoClient.getDatabase("ece568");
        MongoCollection<Document> collection = mongoDatabase.getCollection("realtime");
        
        Block<Document> addToList = new Block<Document>() {
	        @Override
	        public void apply(final Document document) {
	            String temp = document.get("price").toString();
	            BigDecimal price = new BigDecimal(temp);

	            RealTimeStock stock = new RealTimeStock(document.getString("symbol"), price);
	            list.add(stock);
	        }
        };
        
        // query each stock and get the latest price
        for(String s: STOCK_LIST) {
        		collection.find(eq("symbol", s))
        		.sort(Sorts.descending("timestamp"))
        		.limit(1)
        		.forEach(addToList);
        		System.out.println(s + "添加成功");
        }
        

        return list;
	}
}
