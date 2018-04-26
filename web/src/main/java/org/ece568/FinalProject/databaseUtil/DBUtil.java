package org.ece568.FinalProject.databaseUtil;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.ws.rs.core.Response;

import org.ece568.FinalProject.model.Comment;
import org.ece568.FinalProject.model.RealTimeStock;
import org.json.JSONObject;

import com.mongodb.client.model.Aggregates;
import com.mongodb.client.model.Projections;
import com.mongodb.Block;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.MongoServerException;
import com.mongodb.client.AggregateIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import static com.mongodb.client.model.Accumulators.*;
import static com.mongodb.client.model.Aggregates.*;
import static com.mongodb.client.model.Filters.*;
import static com.mongodb.client.model.Projections.*;


import com.mongodb.client.model.Aggregates;
import com.mongodb.client.model.Sorts;
import static java.util.Arrays.asList;

import org.bson.Document;


public class DBUtil {
	public final String[] STOCK_LIST = {"GOOG", "AABA", "FB", "MSFT", "TWTR", "AAPL", "JPM", "AMZN", "JNJ", "BAC"};
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
	
	
	// 返回三种特殊值， min max avg
	public Response getAvg(final String symbol) {
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
		    		valueObj.put("avg", document.get("avg"));
		    		mainObj.put("value", valueObj);
	        }
        };
        
        collection.aggregate(
    				asList(
    				          new Document("$match", new Document("symbol", symbol)),
    					      new Document("$sort", new Document("timestamp", -1)),
    					      new Document("$limit", 252),
    					      group(
       					           "_id:0",
       					           avg("avg", "$close")   
       					      )
    					   )
	).forEach(addToList);
        
		return Response.status(200).entity(mainObj.toString()).build();
	}
	
	// 返回三种特殊值， min max avg
	public Response getMax(final String symbol) {
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
       					           max("max", "$high")
       					      )
    					   )
	).forEach(addToList);
        
		return Response.status(200).entity(mainObj.toString()).build();
	}
	
	// 返回三种特殊值， min max avg
	public Response getMin(final String symbol) {
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
		    		valueObj.put("low", document.get("min"));
		    		
		    		mainObj.put("value", valueObj);
	        }
        };
        
        collection.aggregate(
    				asList(
    				          new Document("$match", new Document("symbol", symbol)),
    					      new Document("$sort", new Document("timestamp", -1)),
    					      new Document("$limit", 252),
    					      group(
       					           "_id:0",
       					           min("min", "$low")         
       					      )
    					   )
	).forEach(addToList);
        

		return Response.status(200).entity(mainObj.toString()).build();
	}
	
	public Response getDay(final String symbol) {
		final JSONObject mainObj = new JSONObject();
		MongoClient mongoClient = new MongoClient(new MongoClientURI(URL));

        // connecting to mongodb
        MongoDatabase mongoDatabase = mongoClient.getDatabase("ece568");
        MongoCollection<Document> collection = mongoDatabase.getCollection("realtime");

        final List<String> timeList = new ArrayList<>();
        final List<String> priceList = new ArrayList<>();
        final List<String> volumeList = new ArrayList<>();
        
        JSONObject dataObj = new JSONObject();
        Block<Document> addToList = new Block<Document>() {
	        @Override
	        public void apply(final Document document) {
		    		mainObj.put("symbol", symbol);
		    		
		    		timeList.add(document.get("timestamp").toString());
		    		priceList.add(document.get("price").toString());
		    		volumeList.add(document.get("volume").toString());
	        }
        };
        
        MongoCursor<Document> output = collection.find(
        		eq("symbol",symbol)).sort(Sorts.descending("timestamp")).limit(9000).iterator();
        
		mainObj.put("symbol", symbol);
		
        int i = 0;
        while(output.hasNext()) {
        		i++;
        		Document temp = output.next();
        		if(i % 150 == 0) {
		    		timeList.add(temp.get("timestamp").toString());
		    		priceList.add(temp.get("price").toString());
		    		volumeList.add(temp.get("volume").toString());
        		}
        }
        
        Collections.reverse(timeList);
        Collections.reverse(priceList);
        Collections.reverse(volumeList);
        
        dataObj.put("time", timeList);
        dataObj.put("price", priceList);
        dataObj.put("volume", volumeList);
        mainObj.put("data", dataObj);
		return Response.status(200).entity(mainObj.toString()).build();
	}
	
	
	
	public Response getMonth(final String symbol) {
		final JSONObject mainObj = new JSONObject();
		MongoClient mongoClient = new MongoClient(new MongoClientURI(URL));

        // connecting to mongodb
        MongoDatabase mongoDatabase = mongoClient.getDatabase("ece568");
        MongoCollection<Document> collection = mongoDatabase.getCollection("daily");

        final List<String> timeList = new ArrayList<>();
        final List<String> priceList = new ArrayList<>();
        final List<String> volumeList = new ArrayList<>();
        
        JSONObject dataObj = new JSONObject();
        Block<Document> addToList = new Block<Document>() {
	        @Override
	        public void apply(final Document document) {
		    		mainObj.put("symbol", symbol);
		    		
		    		timeList.add(document.get("timestamp").toString());
		    		priceList.add(document.get("close").toString());
		    		volumeList.add(document.get("volume").toString());
	        }
        };
        
        collection.find(
        		eq("symbol",symbol)
        		).sort(Sorts.descending("timestamp")).limit(23).forEach(addToList);
        
        Collections.reverse(timeList);
        Collections.reverse(priceList);
        Collections.reverse(volumeList);
        
        dataObj.put("time", timeList);
        dataObj.put("price", priceList);
        dataObj.put("volume", volumeList);
        mainObj.put("data", dataObj);
		return Response.status(200).entity(mainObj.toString()).build();
	}
	

	public Response getYear(final String symbol) {
		final JSONObject mainObj = new JSONObject();
		MongoClient mongoClient = new MongoClient(new MongoClientURI(URL));

        // connecting to mongodb
        MongoDatabase mongoDatabase = mongoClient.getDatabase("ece568");
        MongoCollection<Document> collection = mongoDatabase.getCollection("daily");

        final List<String> timeList = new ArrayList<>();
        final List<String> priceList = new ArrayList<>();
        final List<String> volumeList = new ArrayList<>();
        
        JSONObject dataObj = new JSONObject();
        Block<Document> addToList = new Block<Document>() {
	        @Override
	        public void apply(final Document document) {
		    		mainObj.put("symbol", symbol);
		    		
		    		timeList.add(document.get("timestamp").toString());
		    		priceList.add(document.get("close").toString());
		    		volumeList.add(document.get("volume").toString());
	        }
        };
        
        MongoCursor<Document> output = collection.find(
        		eq("symbol",symbol)
        		).sort(Sorts.descending("timestamp")).limit(252).iterator();
        
        
        int i = 0;
        while(output.hasNext()) {
        		i++;
        		Document temp = output.next();
        		if(i % 7 == 0) {
		    		timeList.add(temp.get("timestamp").toString());
		    		priceList.add(temp.get("close").toString());
		    		volumeList.add(temp.get("volume").toString());
        		}
        }
        
        Collections.reverse(timeList);
        Collections.reverse(priceList);
        Collections.reverse(volumeList);
        
        dataObj.put("time", timeList);
        dataObj.put("price", priceList);
        dataObj.put("volume", volumeList);
        mainObj.put("data", dataObj);
		return Response.status(200).entity(mainObj.toString()).build();
	}
	
	public Response addComment(String symbol, String comment, String timestamp, String username) {
		MongoClient mongoClient = new MongoClient(new MongoClientURI(URL));

        // connecting to mongodb
        MongoDatabase mongoDatabase = mongoClient.getDatabase("ece568");
        MongoCollection<Document> collection = mongoDatabase.getCollection("comment");
        
        Document document = new Document("symbol", symbol)
        		.append("username", username)
        		.append("comment", comment)
        		.append("timestamp", timestamp);
        
        boolean isRegister=true;
        try {
          collection.insertOne(document);
          }
          catch (MongoServerException ex) {
            isRegister=false;
          }
       
        
        JSONObject mainObj = new JSONObject();
        if (isRegister) {
        		mainObj.put("status", "true");
        } else {
        		mainObj.put("status", "false");
        }
        System.out.println();
		return Response.status(200).entity(mainObj.toString()).build();
	}
	
	public Response getComment(String symbol) {
		MongoClient mongoClient = new MongoClient(new MongoClientURI(URL));
		JSONObject mainObj = new JSONObject();

        // connecting to mongodb
        MongoDatabase mongoDatabase = mongoClient.getDatabase("ece568");
        MongoCollection<Document> collection = mongoDatabase.getCollection("comment");
        final List<Comment> list = new ArrayList<>();
        
        Block<Document> addToList = new Block<Document>() {
	        @Override
	        public void apply(final Document document) {
	        		String timestamp = document.getString("timestamp");
	        		String username = document.getString("username");
	        		String symbol = document.getString("symbol");
	        		String comment = document.getString("comment");
	        		
	        		list.add(new Comment(symbol,comment, timestamp, username));
	        }
        };
        
        collection.find(
        		eq("symbol",symbol)
        		).sort(Sorts.descending("timestamp")).limit(5).forEach(addToList);
        
        
        mainObj.put("comment", list);
		return Response.status(200).entity(mainObj.toString()).build();
	}

	public Response getLowerAvgSymbol(final String symbol) {
		MongoClient mongoClient = new MongoClient(new MongoClientURI(URL));
		final JSONObject mainObj = new JSONObject();
        final List<String> list = new ArrayList<>();
        final JSONObject lowPrice = new JSONObject();
        final Map<String, String> avgMap = new HashMap<>();
		final Map<String, String> map = new HashMap();
		//
        // connecting to mongodb
        MongoDatabase mongoDatabase = mongoClient.getDatabase("ece568");
        MongoCollection<Document> collection = mongoDatabase.getCollection("daily");	
        
      Block<Document> addLow = new Block<Document>() {
        @Override
        public void apply(final Document document) {
        		lowPrice.put(symbol, document.get("min"));
        		System.out.println("lowest + " + document.get("_id").toString() + " " + document.get("min"));

        }
    };
        
        Block<Document> addAvg = new Block<Document>() {
	        @Override
	        public void apply(final Document document) {
        			avgMap.put(document.get("_id").toString(), document.get("avg").toString());

	        		System.out.println("avg + " + document.get("_id").toString() + " " + document.get("avg"));
	        }
        };
        
      collection.aggregate(
  				asList(
  				          new Document("$match", new Document("symbol", symbol)),
  					      new Document("$sort", new Document("timestamp", -1)),
					      new Document("$limit", 252),
  					      group(
     					           "$symbol" ,
     					           min("min", "$low")         
     					      )
  					   )
      		).forEach(addLow);
        
        for (String s: STOCK_LIST) {
	        collection.aggregate(
	    				asList(
	    				          new Document("$match", new Document("symbol", s)),
	    					      new Document("$sort", new Document("timestamp", -1)),
	    					      new Document("$limit", 252),
	    					      group(	
	    					    		  	   "$symbol",
	       					           avg("avg", "$close")   
	       					      )
	    					   )
	        		).forEach(addAvg);
        }
        
        System.out.println("test");
      for (Map.Entry<String, String> entry : avgMap.entrySet()) {
    	  if (Double.valueOf(entry.getValue()) < Double.valueOf(lowPrice.get(symbol).toString())) {
			list.add(entry.getKey());
		
		}
      mainObj.put("Stock List", list);
      }
        
        
		return Response.status(200).entity(mainObj.toString()).build();
	}
	

}
