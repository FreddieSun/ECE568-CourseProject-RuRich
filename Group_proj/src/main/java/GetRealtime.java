

import org.json.JSONArray;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;

import java.net.URL;
import java.sql.*;
import java.util.*;
import java.util.Date;

public class GetRealtime {
    private String[] stockList = {"FB"};
    // param for JDBC
    static final String JDBC_DRIVER="com.mysql.jdbc.Driver";
    static final String DB_URL="jdbc:mysql://localhost:3306/ECE568";


    // username and the passname for the databse
    static final String USER="root";
    static final String PASS="";
    static final String apiKey = "DBIUONIEQZL8SQKS";
    static final int timeout = 3000;
    Timer timer;


    public GetRealtime() {
        timer = new Timer();
        timer.schedule(new GetRealTimerTask(), 0, 1000*60);

    }


    public class GetRealTimerTask extends TimerTask {
        @Override
        public void run() {
            Date date = new Date(this.scheduledExecutionTime());
            System.out.println("Current Time is: " + date);

            Connection conn = null;
            Statement stmt = null;
            System.out.println("Please ");
            // 注册 JDBC 驱动
            try {
                Class.forName("com.mysql.jdbc.Driver");
            } catch (ClassNotFoundException e) {
                e.printStackTrace();
            }

            try {

                //链接数据库

                conn = DriverManager.getConnection(DB_URL,USER,PASS);

                //连接API接口
                URL url =new URL("https://www.alphavantage.co/query?function=BATCH_STOCK_QUOTES&symbols=FB&apikey=DBIUONIEQZL8SQKS");
                HttpURLConnection httpURLConnectionconn = (HttpURLConnection) url.openConnection();
                httpURLConnectionconn.setRequestMethod("GET");

                int resultCode = httpURLConnectionconn.getResponseCode();
                System.out.println("Sending 'GET' Request to URL:" + url);
                System.out.println("Resonponse Code:" + resultCode);
                InputStream inputStream = httpURLConnectionconn.getInputStream();
                InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
                BufferedReader in = new BufferedReader(inputStreamReader);
                String inputLine;
                StringBuffer response = new StringBuffer();
                while((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();

                // READ JSON response and print
                JSONObject myResponse = new JSONObject(response.toString());
                System.out.println("result after Reading JSON Response");
                System.out.println(myResponse);

                JSONArray stockInfo = myResponse.getJSONArray("Stock Quotes");

                // the object to extract information
                JSONObject stockInfo1 = (JSONObject) stockInfo.get(0);



                String stockSymbol = stockList[0];

                PreparedStatement psql;
                psql = conn.prepareStatement("INSERT INTO RealTime (symbol, Price, StockTimeStamp, Volume) "
                        +"values(?,?,?,?)");



                psql.setString(1,stockSymbol);
                psql.setString(2,stockInfo1.getString("2. price"));
                psql.setString(3,stockInfo1.getString("4. timestamp"));
                psql.setString(4,stockInfo1.getString("3. volume"));
                psql.execute();

            }catch(SQLException se){
                // 处理 JDBC 错误
                se.printStackTrace();
            }catch(Exception e){
                // 处理 Class.forName 错误
                e.printStackTrace();
            }
            try {
                conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}
