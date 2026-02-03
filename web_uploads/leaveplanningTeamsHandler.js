/****************************************************

 * @description :  The "leaveplanning team handler"

 ***************************************************/

define(
    '@{mvn:widget.web.context.path}/leaveplanningTeamsHandler.js',
    function () {
        'use strict';
        const
            manAvatar = '/theme/images/blank-avatar-man.jpg',
            womanAvatar = '/theme/images/blank-avatar-women.jpg',
            blankAvatar = "/theme/images/blank-avatar.jpg";
        var localizer;
		var key = "";
        var _that;
		var iconZoomDesktop = '<span class = "zoom">' +
                '<svg aria-hidden="true" style="pointer-events: none;" class="popupuser shrs-button__icon shrs-icon shrs-icon_size_medium">' +
                '<use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#shrs-icon-zoom-in"></use>' +
                '</svg>' + '</span>';
        var iconZoomMobile = '<svg aria-hidden="true" style="pointer-events: none;" class="zoom popupuser shrs-button__icon shrs-icon shrs-icon_size_medium">' +
                '<use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#shrs-icon-zoom-in"></use>' +
                '</svg>';

        var leaveplanningTeamsHandler = function (_localizer, _isMobile) {
			this.isMobile = _isMobile;
			_that = this;
            localizer = _localizer; // NOSONAR
            this.iconZoom = this.isMobile ? iconZoomMobile : iconZoomDesktop;
        };
        /**
         * @public Initialize the  leaveplanningTeamsHandler
         * @returns {undefined}
         */
        leaveplanningTeamsHandler.prototype.init = function () { };
        /**
         * generate label for each member
         * @returns label
         */
        leaveplanningTeamsHandler.prototype.getLabel = function (orgUnit,
            memberKey, avatar, labelName, enableIcon) {
            const icon = enableIcon ? _that.iconZoom : '';
            return '<div id="' + orgUnit + '_' + memberKey +
                '"><img src="' +
                avatar +
                '" alt="avatar" class="popupuser b-neutral b-2x rounded"></a><span class="popupuser">' +
                labelName + '</span>' + icon + '</div>';
        };
        /**
         * generate unique id for an element
         * @returns String unique id
         */
        var guid = function () {
            function s4() {
                return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
            }
            return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
        };
        /**
         * generate collab section properties
         * @returns Object collab
         */
        var generateCollabSection = function (
            teams,
            collab, employeeOrgUnit,
            employeesMatcle,
            employeesMatcleSoccleId,
            employeesUoMatcle) {
            var memberCollab = {};

            var memberKey = collab.employeeId;
            var orgUnit;
            if (teams.length === 1) {
                orgUnit = teams[0].orgUnit.code;
            } else {
                if (teams[0].orgUnit.code === employeeOrgUnit.orgUnits[0].code) {
                    orgUnit = teams[0].orgUnit.code;
                } else {
						if(_that.isMobile){
							orgUnit = teams[1].orgUnit.code;
						}
                    orgUnit = employeeOrgUnit.orgUnits[0].code;
                }
            }

            // remove sapces from UO code
            orgUnit = orgUnit.replace(/\s/g, '');
            memberCollab.key = orgUnit + '_' + memberKey.trim();

            var labelName = collab.givenName + ' ' + collab.surName;
            memberCollab.name = labelName;
            if (collab.gender !== null) {
                memberCollab.gender = collab.gender.code;
            }
            if (collab.qualifications !== null && collab.qualifications.qualification[0] !== null) {
                memberCollab.qualification = collab.qualifications.qualification[0].label;
            }
            if (collab.photo !== null) {
                memberCollab.img = 'data:image/gif;base64,' + collab.photo;
            } else if (memberCollab.gender === '1') {
                memberCollab.img = manAvatar;
            } else if (memberCollab.gender === '2') {
                memberCollab.img = womanAvatar;
            } else {
                member.img = blankAvatar;
            }
            memberCollab.label = _that.getLabel(orgUnit, memberKey, memberCollab.img, labelName, true);
            var employeeId = collab.employeeId;
            if (_that.isMobile && employeeId != null && employeeId.indexOf(collab.soccleId) !== 0) {
                employeeId = collab.soccleId + collab.employeeId;
            }

            var findEmployeeId = _.find(employeesMatcle, _.matchesProperty('employeeId', employeeId));
            if (findEmployeeId === undefined) {
                employeesMatcle.push({
                    'employeeId': employeeId
                });
            }

            employeesMatcleSoccleId.push({
                'employeeId': collab.employeeId
            });
            employeesUoMatcle.push({
                'matcle': collab.employeeId,
                'orgUnit': orgUnit,
                'soccle': collab.soccleId,
                'soccleMatcle': collab.employeeId
            });

            return memberCollab;
        };
        /**
         * generate teams section properties
         * @returns Object teams
         */
        var generateTeamsSection =
            function (teams, collab, employeesMatcle, employeesMatcleSoccleId, employeesUoMatcle, employeeManagerId) {

                var sectionList = [];
                for (var indexTeam = 0; indexTeam < teams.length; indexTeam++) {
                    var teamMembers = [];
                    var members = teams[indexTeam].members.member;
                    // get UO code
                    var orgUnit = teams[indexTeam].orgUnit.code;
                    // remove sapces from UO code
                    orgUnit = orgUnit.replace(/\s/g, '');
                    for (var indexMember = 0; indexMember < members.length; indexMember++) {
                        var member = {};
                        var memberKey = members[indexMember].employeeId;
                        member.key = orgUnit + '_' + memberKey.trim();
                        member.orgUnit = teams[indexTeam].orgUnit.code;
                        var labelName = members[indexMember].givenName + ' ' + members[indexMember].surName;
                        member.name = labelName;
                        if (members[indexMember].gender !== null) {
                            member.gender = members[indexMember].gender.code;
                        }
                        if (members[indexMember].employeeId === employeeManagerId) {
                            member.role = 'manager';
                        }
                        if (members[indexMember].qualifications !== null) {
                            member.qualification =
                                members[indexMember].qualifications.qualification[0].label;
                        }
                        if (members[indexMember].photo !== null) {
                            member.img = 'data:image/gif;base64,' + members[indexMember].photo;
                        } else if (member.gender === '1') {
                            member.img = manAvatar;
                        } else if (member.gender === '2') {
                            member.img = womanAvatar;
                        } else {
                            member.img = blankAvatar;
                        }
                        member.label = _that.getLabel(orgUnit, memberKey, member.img, labelName, false);
                        teamMembers.push(member);
                        var employeeId = members[indexMember].employeeId;
                        if (employeeId != null) {
                            employeeId = members[indexMember].employeeId;
                        }
                        employeesMatcle.push({
                            'employeeId': employeeId
                        });
                        employeesMatcleSoccleId.push({
                            'employeeId': members[indexMember].employeeId
                        });
                        employeesUoMatcle.push({
                            'matcle': members[indexMember].employeeId,
                            'orgUnit': orgUnit,
                            'soccle': members[indexMember].soccleId,
                            'soccleMatcle': members[indexMember].employeeId
                        });
                       
                    }
					if(!_that.isMobile){
						key = "-" + guid();
					}
                    var team = {
                        'key': teams[indexTeam].orgUnit.code + key,
                        'label': teams[indexTeam].orgUnit.label,
                        'open': true,
                        'children': teamMembers,
                        'delegated': teams[indexTeam].delegated
                    };
                    sectionList.push(team);
                }
                return sectionList;
            };
        /**
         * @public createTeams
         * @returns {undefined}
         */
        leaveplanningTeamsHandler.prototype.createTeams =
            function (teams, collab, employeeOrgUnit, employeeId, employeesMatcle,
                employeesMatcleSoccleId, employeesUoMatcle, employeeManagerId) {
                var members = [];
                // collab section
                var collabOfTheTeam =
                    generateCollabSection(teams, collab, employeeOrgUnit, employeesMatcle, employeesMatcleSoccleId,
                        employeesUoMatcle);
                members.unshift(collabOfTheTeam);
                // teams section
                var allTeams =
                    generateTeamsSection(teams, collab, employeesMatcle, employeesMatcleSoccleId,
                        employeesUoMatcle, employeeManagerId);
                for (var indexTeam = 0; indexTeam < allTeams.length; indexTeam++) {
                    members.push(allTeams[indexTeam]);
                }

                // fix height of fixed section
                var height_adjust = {
                    'key': 'height_adjust' + guid(),
                    'role': 'height_adjust'
                };
				if(!_that.isMobile){
					members.push(height_adjust);
				}
                return members;
            };
        
        return leaveplanningTeamsHandler;
    });
