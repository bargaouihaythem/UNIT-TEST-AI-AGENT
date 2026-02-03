/**
 * 
 */
package com.soprahr.foryou.hub.model.hra.dsteammgt.hra.dao;

import java.util.Date;
import java.util.List;
import java.util.Map;

import com.soprahr.foryou.hub.model.bc.teammgt.model.orgUnit.OrgUnit;
import com.soprahr.foryou.hub.model.bc.teammgt.service.response.OrgUnitResponse;
import com.soprahr.foryou.hub.model.bc.teammgt.service.response.OrgUnitsResponse;
import com.soprahr.foryou.hub.model.bc.teammgt.service.response.SubOrgUnitResponse;
  
 
 
/**
 * The Interface IHraTransportationModeDao.
 *
 * @author sOueslati
 */
public interface IHraOrgUnitsDao extends IHraGenericDao<OrgUnit, String, String, String> {

	OrgUnitsResponse getOrgUnitsLabel(String idUO,String personId,String vsid);
	Map<Object, Object> getOrgUnitsLabelByCode(List<String> subOrgUnitCodeLists);
	
	OrgUnitResponse getManagerOrgUnits(String personId,String vsid);

	SubOrgUnitResponse getManagedSubOrgUnits(String personId);
	
	OrgUnitResponse getOrgUnits(String personId, Date beginDate, Date endDate, boolean directOnly);
}
