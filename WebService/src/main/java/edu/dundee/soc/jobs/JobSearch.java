package edu.dundee.soc.jobs;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.json.JSONArray;
import org.json.JSONException;

@WebServlet(name = "JobSearch", urlPatterns = {"/*"})
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

        response.setContentType("application/javascript");

        //Extract params from request
        String[] industry = request.getParameterValues("industry"); //Can specify multiple parameters
        String location = request.getParameter("location");
        String hours = request.getParameter("hours");
        String employer = request.getParameter("employer");
        String longitude = request.getParameter("longitude");
        String latitude = request.getParameter("latitude");

        DatabaseConnector db = new DatabaseConnector();
        
        if (longitude == null || latitude == null) {
            try {
                //Execute db query
                ResultSet rs = db.find(industry, location);
                printResultSet(response, rs);
            } catch (SQLException e) {
                System.err.println("Error while printing result set: " + e.toString());
            }
        }else{
            try {
                //Execute db query
                ResultSet rs = db.find(industry, latitude, longitude);
                printResultSet(response, rs);
            } catch (SQLException e) {
                System.err.println("Error while printing result set: " + e.toString());
            }
        }
    }

    /**
     * Convert db response to JSON
     * @param response
     * @param rs 
     */
    private void printResultSet(HttpServletResponse response, ResultSet rs) {
        try {        
            PrintWriter outputStream = response.getWriter();
            JSONArray json = ResultSetConverter.convert(rs);
            String jsonString = json.toString();
            jsonString = "callback(" + jsonString + ");";
            outputStream.print(jsonString);
        } catch (JSONException ex) {
            Logger.getLogger(JobSearch.class.getName()).log(Level.SEVERE, null, ex);
        } catch (SQLException e) {
            System.err.println("Error while printing result set: " + e.toString());
        } catch (IOException e){
            Logger.getLogger(JobSearch.class.getName()).log(Level.SEVERE, null, e);
        }
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
