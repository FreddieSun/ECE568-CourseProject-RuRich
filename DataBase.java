import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;


public class DataBase {

	private Connection conn;
	private java.sql.Statement stmt;
	
		DataBase()
		{
			try {
				Class.forName("com.mysql.jdbc.Driver");// 第一步,加载类
				//long start=System.currentTimeMillis();
				conn=DriverManager.getConnection("jdbc:mysql://localhost:3306/stockinformation?characterEncoding=utf8&useSSL=true","root","Zhy19960102");//第二步，建立连接
				//long end=System.currentTimeMillis();
				stmt=conn.createStatement();
				//System.out.println(conn);
				//System.out.println("耗时"+(end-start)+"ms");//建立连接是很耗时间的,后期会改用连接池来做
	 
			
			} catch (ClassNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		public Connection getConn() {
			return conn;
		}
		public java.sql.Statement  getStmt() {
			return  stmt;
		}
		
}