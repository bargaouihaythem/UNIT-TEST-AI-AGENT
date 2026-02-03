package com.soprahr.foryou.hub.model.hra.dsteammgt.hra;

import com.soprahr.foryou.hub.model.bc.teammgt.service.IColleaguesService;
import com.soprahr.foryou.hub.model.bc.teammgt.service.response.TeamsResponse;
import com.soprahr.foryou.hub.model.hra.dsteammgt.hra.dao.IHRaColleaguesDao;

public class ColleaguesServiceImpl implements IColleaguesService {

	private IHRaColleaguesDao colleaguedaoimpl;

	public IHRaColleaguesDao getColleaguedaoimpl() {
		return colleaguedaoimpl;
	}

	public void setColleaguedaoimpl(IHRaColleaguesDao colleaguedaoimpl) {
		this.colleaguedaoimpl = colleaguedaoimpl;
	}

	public TeamsResponse getColleaguesMembers(String personId) {

		TeamsResponse response;

		response = colleaguedaoimpl.getColleaguesMembers(personId);
		return response;

	}

}
