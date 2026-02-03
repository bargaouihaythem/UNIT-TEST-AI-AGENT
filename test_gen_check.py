"""Test du générateur pour vérifier les tests Mockito"""
from smart_test_generator import SmartTestGenerator

code = '''
package com.soprahr.foryou.hub.model.hra.dsteammgt.hra;
import java.util.Date;
import com.soprahr.foryou.hub.model.hra.dsteammgt.hra.dao.IHraOrgUnitsDao;

public class OrgUnitsServiceImpl {
    private IHraOrgUnitsDao orgUnitsDaoImpl;

    public String getIdentification() {
        return "OrgUnitsServiceImpl";
    }

    public OrgUnitsResponse getOrgUnitsLabel(String idUO, String personId, String vsid) {
        return orgUnitsDaoImpl.getOrgUnitsLabel(idUO, personId, vsid);
    }

    public IHraOrgUnitsDao getOrgUnitsDaoImpl() {
        return orgUnitsDaoImpl;
    }

    public void setOrgUnitsDaoImpl(IHraOrgUnitsDao orgUnitsDaoImpl) {
        this.orgUnitsDaoImpl = orgUnitsDaoImpl;
    }

    public OrgUnitResponse getManagerOrgUnits(String personId, String vsid) {
        return orgUnitsDaoImpl.getManagerOrgUnits(personId, vsid);
    }

    public SubOrgUnitResponse getManagedSubOrgUnits(String personId) {
        return orgUnitsDaoImpl.getManagedSubOrgUnits(personId);
    }

    public OrgUnitResponse getOrgUnits(String personId, Date beginDate, Date endDate, boolean directOnly) {
        return orgUnitsDaoImpl.getOrgUnits(personId, beginDate, endDate, directOnly);
    }
}
'''

gen = SmartTestGenerator(code, 'OrgUnitsServiceImpl.java', use_ai=False)
tests = gen.generate()
print(tests)
