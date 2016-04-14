package database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import models.Tweet;


public class Repo {
	
	Connection conn;
	final static String DB_URL = "jdbc:sqlite:res/tweets.db";
	
	public void connect(){
		try {	
			conn = DriverManager.getConnection(DB_URL);
			
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	public List<Tweet> getTweets(int limit){
		
		List<Tweet> tweets = new ArrayList<>();
		
		try {
			String query;
			if(limit==-1){
				query = "SELECT * FROM tweets;";
			}
			else{
				query = "SELECT * FROM tweets LIMIT "+limit+";";				
			}
			Statement st = conn.createStatement();
			ResultSet rs = st.executeQuery(query);
			while(rs.next()){
				String content = rs.getString("content");
				String id = rs.getString("id");
				String username = rs.getString("username");
				String time = rs.getString("timestamp");
				
				Tweet t = new Tweet();
				t.setContent(content);
				t.setId(id);
				t.setUsername(username);
				t.setTimestamp(time);
				tweets.add(t);
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return tweets;
		
	}

}
