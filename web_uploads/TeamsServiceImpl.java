/**
 * 
 */
package com.soprahr.foryou.hub.model.hra.dsteammgt.hra;

import java.util.Date;
import java.util.List;

import com.soprahr.foryou.hub.model.bc.teammgt.service.ITeamsService;
import com.soprahr.foryou.hub.model.bc.teammgt.service.request.TeamsRequest;
import com.soprahr.foryou.hub.model.bc.teammgt.service.response.EmployeesResponse;
import com.soprahr.foryou.hub.model.bc.teammgt.service.response.TeamsResponse;
import com.soprahr.foryou.hub.model.hra.dsteammgt.hra.dao.IHraTeamsDao;

//Auto-generated Javadoc
/**
 * The Class TransportationModeServiceImpl.
 *
 * @author sOueslati
 */
public class TeamsServiceImpl implements ITeamsService
{

    /** The transportation mode dao impl. */
    private IHraTeamsDao teamsDaoImpl;

    @Override
    public String getIdentification()
    {
        return "TeamsServiceImpl";
    }
    
    @Override
    public TeamsResponse getTeamsMembers( String personId, List<TeamsRequest> teamsRequest, String vsid )
    {
        return teamsDaoImpl.getTeamMembers( personId, teamsRequest, vsid );
    }
    
    @Override
    public TeamsResponse getSubTeamsMembers( String personId, List<TeamsRequest> teamsRequest)
    {
        return teamsDaoImpl.getSubTeamMembers( personId, teamsRequest);
    }

    @Override
    public EmployeesResponse getMembers(String fields, String vsid) {
        return teamsDaoImpl.getMembers(fields, vsid);
    }


    public IHraTeamsDao getTeamsDaoImpl()
    {
        return teamsDaoImpl;
    }

    public void setTeamsDaoImpl( IHraTeamsDao teamsDaoImpl )
    {
        this.teamsDaoImpl = teamsDaoImpl;
    }
    
    @Override
	public EmployeesResponse getEndOfContractTeamMembersByUO(String field, String vsid) {
    	return teamsDaoImpl.getEndOfContractTeamMembersByUO(field, vsid);
	}

    @Override
    public EmployeesResponse getAllAvailableContractTeamMembersByUO(String field) {
        return teamsDaoImpl.getAllAvailableContractTeamMembersByUO(field);
    }

    @Override
    public EmployeesResponse getTeamMembersInProbationByUO(String field, String vsid) {
        return teamsDaoImpl.getTeamMembersInProbationByUO(field,vsid);
    }

	@Override
	public long getTeamMembersInProbationByUOCount(String vsid, int resultLimit) {
        return teamsDaoImpl.getTeamMembersInProbationByUOCount(vsid, resultLimit);
	}

    @Override
    public EmployeesResponse getTeamMembersForTermination(String field, String vsid, int myId) {
        return teamsDaoImpl.getTeamMembersForTermination(field, vsid,myId);
    }

    @Override
    public TeamsResponse getAllMembersForAllowance(String field, String personId,List<TeamsRequest> teamsRequest) {
        return teamsDaoImpl.getAllMembersForAllowance(field, personId,teamsRequest);
    }

	@Override
	public TeamsResponse getAllTeamsMembers(String personId, List<TeamsRequest> teamsRequest, Date beginDate,
			Date endDate) {
		return teamsDaoImpl.getAllTeamsMembers(personId, teamsRequest, beginDate, endDate);
	}
}
