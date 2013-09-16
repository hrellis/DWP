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
        setValues(statement, industry);        
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
    public static void setValues(PreparedStatement preparedStatement, String... values) throws SQLException {
        for (int i = 0; i < values.length; i++) {
            preparedStatement.setObject(i + 2, values[i]);
        }
    }
}