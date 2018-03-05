import java.io.IOException;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;

/**
 * ≤‚ ‘¿‡
 */

public class Test {
	public static void main(String[] args) throws IOException, SQLException, InterruptedException {
		GetStock stockUtil = new GetStock();
		DataBase DB = new DataBase();
		Statement stat = DB.getStmt();
		stat.execute("delete from information");
		stat.execute("delete from information_his");
		String[] stockList = new String[] { "MS","FB",  "AMZN", "MSFT", "GOOG",  "IBM", "INTC", "AMD","BAC","EBAY"};
		System.out.println("Start");
		for (String a : stockList) {
			List<StockData> sd_DAY = stockUtil.getStockCsvData(a,1);
			List<StockData> sd_MONTHLY = stockUtil.getStockCsvData(a,2);
			//Save daily information to the database
			for (StockData x : sd_DAY) {
				String sql = "insert into information (Stock,Date,open_value,high_value,low_value,close_value,volume_value) values ('"
						+ a + "','" + x.getDate() + "' ,'" + x.getOpen() + "','" + x.getHigh() + "','"
						+ x.getLow() + "','" + x.getClose() + "','" + x.getVolume() + "') ";
				stat.execute(sql);
			}
			//Save monthly information to the database
			for (StockData x : sd_MONTHLY) {
				String sql = "insert into information_his (Stock,Date,open_value,high_value,low_value,close_value,volume_value) values ('"
						+ a + "','" + x.getDate() + "' ,'" + x.getOpen() + "','" + x.getHigh() + "','"
						+ x.getLow() + "','" + x.getClose() + "','" + x.getVolume() + "') ";
				stat.execute(sql);
			}
			System.out.println("Finish stock: "+a);
			System.out.println("wait 1 second");
			Thread.sleep(1000);
		}
		System.out.println("Done");

	}
}