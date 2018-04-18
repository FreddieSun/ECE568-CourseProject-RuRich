package org.ece568.FinalProject.databaseUtil;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;

import javax.ws.rs.core.Response;

import org.ece568.FinalProject.model.RealTimeStock;
import org.json.JSONObject;

import com.mongodb.Block;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.AggregateIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import static com.mongodb.client.model.Accumulators.*;
import static com.mongodb.client.model.Aggregates.*;
import static com.mongodb.client.model.Filters.*;
import com.mongodb.client.model.Sorts;
import static java.util.Arrays.asList;

import org.apache.jasper.tagplugins.jstl.core.ForEach;
import org.bson.Document;


public class DBUtil {
	public final String[] STOCK_LIST = {"GOOG", "AABA", "FB", "MSFT", "TWTR", "AAPL", "JPM", "AMZN", "JNJ", "BNC"};

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
	
	
	public Response getDataForFigure(final String symbol) {
		final JSONObject mainObj = new JSONObject();
		MongoClient mongoClient = new MongoClient(new MongoClientURI(URL));

        // connecting to mongodb
        MongoDatabase mongoDatabase = mongoClient.getDatabase("ece568");
        MongoCollection<Document> collection = mongoDatabase.getCollection("daily");
        
        Block<Document> addToList = new Block<Document>() {
	        @Override
	        public void apply(final Document document) {
		    		mainObj.put("symbol", symbol);
		    		
		    		JSONObject valueObj = new JSONObject();
		    		valueObj.put("max", document.get("max"));
		    		valueObj.put("avg", document.get("avg"));
		    		valueObj.put("low", document.get("min"));
		    		
		    		mainObj.put("value", valueObj);
	        }
        };
        
        collection.aggregate(
    				asList(
    				          new Document("$match", new Document("symbol", symbol)),
    					      new Document("$sort", new Document("timestamp", -1)),
    					      new Document("$limit", 10),
    					      group(
       					           "_id:0",
       					           avg("avg", "$close"),
       					           max("max", "$high"),
       					           min("min", "$low")         
       					      )
    					   )
	).forEach(addToList);;
	
//        double maxPrice = Integer.MIN_VALUE;
//        for(Document docObj: output) {
//        		double tempPrice = Double.valueOf(docObj.get("max").toString());
//        		maxPrice = Math.max(tempPrice, maxPrice);
//        }
//        mainObj.put("max", maxPrice);
//        
    	
        
		return Response.status(200).entity(mainObj.toString()).build();
	}
}
