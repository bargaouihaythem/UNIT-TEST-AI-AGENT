/**
 * 
 */
package com.soprahr.foryou.hub.model.hra.dsteammgt.hra;

import java.util.Date;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.soprahr.foryou.hub.model.bc.teammgt.service.IOrgUnitsService;
import com.soprahr.foryou.hub.model.bc.teammgt.service.response.OrgUnitResponse;
import com.soprahr.foryou.hub.model.bc.teammgt.service.response.OrgUnitsResponse;
import com.soprahr.foryou.hub.model.bc.teammgt.service.response.SubOrgUnitResponse;
import com.soprahr.foryou.hub.model.hra.dsteammgt.hra.dao.IHraOrgUnitsDao;


//Auto-generated Javadoc
/**
 * The Class TransportationModeServiceImpl.
 *
 * @author sOueslati
 */
public class OrgUnitsServiceImpl implements IOrgUnitsService {
	
	/** The transportation mode dao impl. */
	private IHraOrgUnitsDao orgUnitsDaoImpl;
	
	@Override
	public String getIdentification() {
		return "OrgUnitsServiceImpl";
	}
	
	@Override
	public OrgUnitsResponse getOrgUnitsLabel(String idUO,String personId, String vsid) {
		OrgUnitsResponse response ;
			response = orgUnitsDaoImpl.getOrgUnitsLabel(idUO,personId, vsid);
			return response;
	}

	public IHraOrgUnitsDao getOrgUnitsDaoImpl() {
		return orgUnitsDaoImpl;
	}

	public void setOrgUnitsDaoImpl(IHraOrgUnitsDao orgUnitsDaoImpl) {
		this.orgUnitsDaoImpl = orgUnitsDaoImpl;
	}
	
    @Override
    public OrgUnitResponse getManagerOrgUnits( String personId, String vsid )
    {
        return orgUnitsDaoImpl.getManagerOrgUnits(personId, vsid);
         
    }

    @Override
    public SubOrgUnitResponse getManagedSubOrgUnits(String personId) {
        return orgUnitsDaoImpl.getManagedSubOrgUnits(personId);
    }

	@Override
	public OrgUnitResponse getOrgUnits(String personId, Date beginDate, Date endDate, boolean directOnly) {
		return orgUnitsDaoImpl.getOrgUnits(personId, beginDate, endDate, directOnly);
	}
}
