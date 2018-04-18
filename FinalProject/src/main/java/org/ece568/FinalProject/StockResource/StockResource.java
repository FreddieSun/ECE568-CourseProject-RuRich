package org.ece568.FinalProject.StockResource;

import java.util.List;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.Response.Status;

import org.ece568.FinalProject.model.RealTimeStock;
import org.ece568.FinalProject.service.StockService;
import org.json.JSONArray;
import org.json.JSONObject;

@Path("StockResource")
public class StockResource {
	
	StockService stockService = new StockService();

    @GET
    @Produces(MediaType.APPLICATION_JSON)
	public List<RealTimeStock> getStockResource() {
    		return stockService.getAllStock();
    }
    
    @GET
    @Path("/{symbol}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getJson(@PathParam("symbol") String symbol) {
    		return stockService.getDataForFigure(symbol);
    }
    
	
}
