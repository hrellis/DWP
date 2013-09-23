package edu.dundee.soc.jobs;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.annotation.Resource;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.sql.DataSource;

@Resource(name = "jdbc/jobs", type = javax.sql.DataSource.class)
public class DatabaseConnector {

    private DataSource ds;
    protected Connection connect;
    private Statement statement;

    /*
     * Loads MySQL Driver and sets DataSource pointer to the 
     * JNDI for the database in web.xml
     */
    public DatabaseConnector() {
        String dbname = "jdbc/jobs";

        try {
            ds = (DataSource) new InitialContext().lookup("java:comp/env/" + dbname);
        } catch (NamingException e) {
            System.err.println(dbname + " is missing: " + e.toString());
        }
    }

    /*
     * Establishes a connection to the database
     */
    public Connection getConnection() {
        try {
            return ds.getConnection();
        } catch (SQLException e) {
            System.err.println("Error while connecting to database: " + e.toString());
        }
        return null;
    }
    
    /*
     * Connects to the database and issues the command
     * @param command which is executed by the database
     */
    public ResultSet execute(String command) {
        try {
            connect = getConnection();
            statement = connect.createStatement();
            statement.execute(command);
            return statement.getResultSet();
        } catch (SQLException e) {
            System.err.println("Error while executing SQL statement" + e.toString());
            return null;
        }
    }

    /**
     * closes any connection open in the connect field
     */
    public void close() {
        try {
            connect.close();
        } catch (SQLException ex) {
            System.err.println("Error while closing db connection" + ex.toString());
        }
    }
    
    
    private static final String SQL_FIND = "SELECT * FROM table_jobs WHERE location LIKE ? AND industry IN (%s);";

    /**
     * Based on http://stackoverflow.com/questions/178479/preparedstatement-in-clause-alternatives
     */
    public ResultSet find(String[] industry, String location) throws SQLException {        
        String sql = String.format(SQL_FIND, preparePlaceHolders(industry.length));
        
        connect = getConnection();
        PreparedStatement statement = connect.prepareStatement(sql);
        statement.setString(1, location);
        setValues(statement, 2, industry);        
        ResultSet resultSet = statement.executeQuery();
        return resultSet;
    }
    
    
    private static final String SQL_FIND_BY_DISTANCE =  "SELECT *, " +
                                                        " ( 3959 * acos( cos( radians( ? )) * cos( radians( latitude )) * " +
                                                        "cos( radians( longitude) - radians( ? )) + " + 
                                                        "sin( radians( ? )) * sin(radians( latitude )))) " +
                                                        "AS distance FROM table_jobs " +
                                                        "WHERE industry IN (%s) " + 
                                                        "AND hide = 0 " +
                                                        "%s" +
                                                        "HAVING distance < ? " +
                                                        "ORDER BY distance;";
    
    public ResultSet find(String[] industry, String lat, String lng, String radius, int hours) throws SQLException {
        String sql;
        switch (hours){
            case 0:
                sql = String.format(SQL_FIND_BY_DISTANCE, preparePlaceHolders(industry.length), "AND part_time = 0 ");
                break;
            case 1:
                sql = String.format(SQL_FIND_BY_DISTANCE, preparePlaceHolders(industry.length), "AND part_time = 1 ");
                break;
            default:
                sql = String.format(SQL_FIND_BY_DISTANCE, preparePlaceHolders(industry.length), "");
        }
        
        connect = getConnection();
        PreparedStatement statement = connect.prepareStatement(sql);
        statement.setString(1, lat);
        statement.setString(2, lng);
        statement.setString(3, lat);
        setValues(statement, 4, industry);
        statement.setString(4 + industry.length, radius);
        
        System.out.println(statement.toString());
        
        ResultSet resultSet = statement.executeQuery();
        return resultSet;
    }
    
    /**
     * Support for adding a variable sized set to a SELECT query
     * http://stackoverflow.com/questions/178479/preparedstatement-in-clause-alternatives
     */
    public static String preparePlaceHolders(int length) {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < length;) {
            builder.append("?");
            if (++i < length) {
                builder.append(",");
            }
        }
        return builder.toString();
    }

    /**
     * http://stackoverflow.com/questions/178479/preparedstatement-in-clause-alternatives
     */
    public static void setValues(PreparedStatement preparedStatement, int startParameter, String... values) throws SQLException {
        for (int i = 0; i < values.length; i++) {
            preparedStatement.setObject(i + startParameter, values[i]);
        }
    }
}
