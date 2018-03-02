import org.patriques.AlphaVantageConnector;
import org.patriques.TimeSeries;
import org.patriques.input.timeseries.Interval;
import org.patriques.input.timeseries.OutputSize;
import org.patriques.output.AlphaVantageException;
import org.patriques.output.timeseries.Daily;
import org.patriques.output.timeseries.IntraDay;
import org.patriques.output.timeseries.data.StockData;
import org.patriques.*;

import java.util.List;
import java.util.Map;
import java.sql.*;

public class GetHistoricalStock {
    // param for JDBC
    static final String JDBC_DRIVER="com.mysql.jdbc.Driver";
    static final String DB_URL="jdbc:mysql://localhost:3306/ECE568";


    // username and the passname for the databse
    static final String USER="root";
    static final String PASS="";


    public static void main(String[] args) throws ClassNotFoundException, SQLException {
        String apiKey = "DBIUONIEQZL8SQKS";
        int timeout = 3000;
        AlphaVantageConnector apiConnector = new AlphaVantageConnector(apiKey, timeout);
        TimeSeries stockTimeSeries = new TimeSeries(apiConnector);

        Connection conn = null;
        Statement stmt = null;
        System.out.println("Please ");
        // 注册 JDBC 驱动
        Class.forName("com.mysql.jdbc.Driver");

        // 打开链接
        System.out.println("连接数据库...");
        conn = DriverManager.getConnection(DB_URL,USER,PASS);
        // 清空数据库
        PreparedStatement deleteStatement;
        deleteStatement = conn.prepareStatement("DELETE FROM HistoricalData");
        deleteStatement.execute();

        String[] stockList = {"FB","APPL","AMZN","MSFT","GOOG","NOK","IBM","ORCL","INTC","AMD"};

        for (int i = 0; i <stockList.length; i++) {
            try{
                String stockSymbol = stockList[i];

                PreparedStatement psql;
                psql = conn.prepareStatement("INSERT INTO HistoricalData (symbol, stockDate, open_val, high_val, low_val, close_val, volume) "
                        +"values(?,?,?,?,?,?,?)");

                //调用API获取数据
                //IntraDay response = stockTimeSeries.intraDay("MSFT", Interval.ONE_MIN, OutputSize.COMPACT);
                Daily response = stockTimeSeries.daily(stockSymbol,OutputSize.COMPACT);
                Map<String, String> metaData = response.getMetaData();
                System.out.println("Symbol" + stockSymbol);
                System.out.println("Information: " + metaData.get("1. Information"));
                System.out.println("Stock: " + metaData.get("2. Symbol"));

                List<StockData> stockData = response.getStockData();

                stockData.forEach(stock -> {
                    System.out.println("date:   " + stock.getDateTime());
                    System.out.println("open:   " + stock.getOpen());
                    System.out.println("high:   " + stock.getHigh());
                    System.out.println("low:    " + stock.getLow());
                    System.out.println("close:  " + stock.getClose());
                    System.out.println("volume: " + stock.getVolume());

                    // 开始写入
                    try {
                        psql.setString(1,stockSymbol);
                        psql.setString(2,stock.getDateTime().toString());
                        psql.setDouble(3,stock.getOpen());
                        psql.setDouble(4,stock.getHigh());
                        psql.setDouble(5,stock.getLow());
                        psql.setDouble(6,stock.getClose());
                        psql.setLong(7,stock.getVolume());
                        psql.execute();
                    } catch (SQLException e) {
                        e.printStackTrace();
                    }
                    //写入成功



                });



            }catch(SQLException se){
                // 处理 JDBC 错误
                se.printStackTrace();
            }catch(Exception e){
                // 处理 Class.forName 错误
                e.printStackTrace();
            }
        }
        conn.close();

    }
}
