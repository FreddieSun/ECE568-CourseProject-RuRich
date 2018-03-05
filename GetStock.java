
/** 
 * yahoo股票数据接口工具类 
 * @ 2013.01.02 
 * @version 1.0 
 */
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class GetStock {

	// public static final String YAHOO_FINANCE_URL =
	// "http://table.finance.yahoo.com/table.csv?";
	public static final String YAHOO_FINANCE_URL = "http://finance.yahoo.com/table.csv?";
	public static final String YAHOO_FINANCE_URL_TODAY = "http://download.finance.yahoo.com/d/quotes.csv?";
	public static final String Sina_FINACE_URL = "http://hq.sinajs.cn/list=sz002218";
	public static final String Alpha_FINACE_MONTHLY_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=";
	public static final String Alpha_FINACE_INTRADAY_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=";
	public static final String Alpha_FINANCE_URL_SETTING = "&interval=1min&apikey=76LUKKYXN127QLZ7&datatype=csv";

	public List<StockData> getStockCsvData(String stockName, int mode) {
		List<StockData> list = new ArrayList<StockData>();
		String url = "";
		String type = "";
		// mode 1: INTRADAY mode
		if (mode == 1) {
			url = Alpha_FINACE_INTRADAY_URL + stockName + Alpha_FINANCE_URL_SETTING;
			type = "_IntraDay";
		}

		// mode 2:MONTHLY mode
		else if (mode == 2) {
			url = Alpha_FINACE_MONTHLY_URL + stockName + Alpha_FINANCE_URL_SETTING;
			type = "_Monthly";
		} else
			return null;
		URL MyURL = null;
		URLConnection con = null;
		InputStreamReader ins = null;
		BufferedReader in = null;
		try {
			MyURL = new URL(url);
			con = MyURL.openConnection();
			ins = new InputStreamReader(con.getInputStream(), "UTF-8");
			in = new BufferedReader(ins);

			String newLine = in.readLine();// 标题行
			String text = "";
			int time = 0;
			while ((newLine = in.readLine()) != null) {
				if (time == 0)
					time++;
				else {
					String[] result = newLine.split(",");
					StockData now = new StockData();
					now.setDate(result[0]);
					now.setOpen(Double.valueOf(result[1]));
					now.setHigh(Double.valueOf(result[2]));
					now.setLow(Double.valueOf(result[3]));
					now.setClose(Double.valueOf(result[4]));
					now.setVolume(Double.valueOf(result[5]));
					list.add(now);
				}
				text += newLine;
				text += "\n";
			}
			// Wtrite into file
			File writename = new File(".\\result\\" + stockName + type + ".csv"); // 相对路径，如果没有则要建立一个新的output。txt文件
			writename.createNewFile(); // 创建新文件
			BufferedWriter out = new BufferedWriter(new FileWriter(writename));
			out.write(text); // \r\n即为换行
			out.flush(); // 把缓存区内容压入文件
			out.close(); // 最后记得关闭文件

		} catch (Exception ex) {
			return null; // 无交易数据
		} finally {
			if (in != null)
				try {
					in.close();
				} catch (IOException ex) {
					ex.printStackTrace();
				}
		}
		return list;
	}

}
