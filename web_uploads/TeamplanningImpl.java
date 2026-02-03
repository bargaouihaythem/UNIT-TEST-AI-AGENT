package com.soprahr.foryou.appl.ch.leave.widget.teamplanning.main;

import java.util.HashMap;
import java.util.Map;

public class TeamplanningImpl implements ITeamplanning {

    private String displaySchoolHolidays;
    private String displaySubHierarchicalService;
    private String displaySubHierarchicalServiceDefault;
    
    @Override
	public  Map<String, String> retrieveConfiguration() {
		Map<String, String> result = new HashMap<>();
		result.put("displaySchoolHolidays", displaySchoolHolidays);
		result.put("displaySubHierarchicalService", displaySubHierarchicalService);
		result.put("displaySubHierarchicalServiceDefault", displaySubHierarchicalServiceDefault);
		return result;
	}

	public String getDisplaySchoolHolidays() {
	return displaySchoolHolidays;
	}

	public void setDisplaySchoolHolidays(String displaySchoolHolidays) {
		this.displaySchoolHolidays = displaySchoolHolidays;
	}

	public String getDisplaySubHierarchicalService() {
		return displaySubHierarchicalService;
	}

	public void setDisplaySubHierarchicalService(String displaySubHierarchicalService) {
		this.displaySubHierarchicalService = displaySubHierarchicalService;
	}
	
	public String getDisplaySubHierarchicalServiceDefault() {
		return displaySubHierarchicalServiceDefault;
	}

	public void setDisplaySubHierarchicalServiceDefault(String displaySubHierarchicalServiceDefault) {
		this.displaySubHierarchicalServiceDefault = displaySubHierarchicalServiceDefault;
	}
}
