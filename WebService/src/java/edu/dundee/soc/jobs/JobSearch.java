package edu.dundee.soc.jobs;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(name = "JobSearch", urlPatterns = {"/JobSearch"})
public class JobSearch extends HttpServlet {

    /**
     * Handles the HTTP
     * <code>GET</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        
        String[] industry = request.getParameterValues("industry"); //Can specify multiple parameters
        String location = request.getParameter("location");
        String hours = request.getParameter("hours");
        String employer = request.getParameter("employer");
        
        DatabaseConnector db = new DatabaseConnector();
        ResultSet rs = db.execute("SELECT * FROM table_jobs");
        
        
        PrintWriter outputStream = response.getWriter();
        
        try{
            outputStream.print(rs.getString("title"));
        } catch (SQLException e) {
            System.err.println("Error while printing result set: " + e.toString());
        }
        
        
        //TODO
        //Connnect to DB
        //Run query
        //Convert to JSON
    }

    /**
     * Handles the HTTP
     * <code>POST</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
    }

    /**
     * Returns a short description of the servlet.
     *
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "Handles job search requests";
    }
}
