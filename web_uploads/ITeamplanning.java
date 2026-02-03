package com.soprahr.foryou.appl.leave.widget.teamplanning.main;

import java.util.Map;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;

public interface ITeamplanning {
    @GET
    @Path( "/config" )
    @Produces ( "application/json" )
    Map<String, String> retrieveConfiguration();
}
