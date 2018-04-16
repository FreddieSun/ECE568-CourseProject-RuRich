package org.ece568.FinalProject.databaseUtil;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;


import org.ece568.FinalProject.model.RealTimeStock;
import org.json.JSONObject;

import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;

import org.bson.Document;


public class DBUtil {
	
    public static final String URL = "mongodb://ece568:ece568project@zwithc.cn:27017";

	/*
	 * 4.1 1. Show the list of all companies in the database 
	 * along with their latest stock price (real time latest stock price)
	 */
	public List<RealTimeStock> getAllStock() {
		List<RealTimeStock> list = new ArrayList<>();
        MongoClient mongoClient = new MongoClient(new MongoClientURI(URL));

        // connecting to mongodb
        MongoDatabase mongoDatabase = mongoClient.getDatabase("ece568");
        System.out.println("连接成功");
        MongoCollection<Document> collection = mongoDatabase.getCollection("realtime");
        
        System.out.println("连接collection成功");

        FindIterable<Document> iterDoc = collection.find();
        MongoCursor<Document> mongoCursor = iterDoc.iterator();
        
//        while (mongoCursor.hasNext()) {
////            String symbol = mongoCursor.next().getString("symbol");
////            String temp = mongoCursor.next().get("price").toString();
////            BigDecimal price = new BigDecimal(temp);
////            RealTimeStock stock = new RealTimeStock(symbol, price);
////            list.add(stock);
//        }
        BigDecimal price = new BigDecimal("123");
        BigDecimal price1 = new BigDecimal("234");


        RealTimeStock stock1 = new RealTimeStock("Google", price);
        RealTimeStock stock2 = new RealTimeStock("Apple", price1);
        list.add(stock1);
        list.add(stock2);
        return list;
	}
}
