/**********************************************************

 * @description :  The "leaveplanning date time picker"

 **********************************************************/
require(['css!/resources/js/lib/qtip/jquery.qtip']);
define('@{mvn:widget.web.context.path}/leaveplanningCustomQtip.js', function(require) {

    'use strict';

    var qtip = require('qtip'), // NOSONAR
        moment = require('moment'),
        Ractive = require('ractive/ractive'),
        deviceHelper = require('common/helpers/deviceHelper'),
        jquery = require('jquery');

    const popupLeaveplanningURL = 'text!@{mvn:widget.web.context.path}/templatePopupLeaveplanningscheduler.html',
        cockpitUrl = 'text!@{mvn:widget.web.context.path}/popUpCockpit.html';
    var popupUserContent,
        cockpit,
		position,
		content,
		clickType = 'click',
		eventParameter = '.zoom',
        _self,
        hideOn;
    /**
     * loadPopUps : load popups resources
     */

    var loadPopUps = function() {

        require([popupLeaveplanningURL],
            function(text) {
                popupUserContent = text;
            },
            function(err) {
                popupUserContent = '';
                logger.error(err);
            }
        );

        require([cockpitUrl],
            function(text) {
                cockpit = text;
            },
            function(err) {
                cockpit = err;
            }
        );
    };

    var leaveplanningCustomQtip = function(phInsId, localizer, _isMobile) {
		this.isMobile = _isMobile;
		_self = this;
        //load all view popups
        loadPopUps();

        this.localizer = localizer;
        if (deviceHelper.is('tablet') || deviceHelper.is('mobile')) {
            hideOn = false;
        } else {
            hideOn = 'unfocus';
        }
    };


    /*  Update widget height */

    var updateHeightWidget = function() {
        jquery.event.trigger({
            type: 'heightUpdate',
            phInstId: 'phInstId'
        });
    };


    function getEligibleBalanceList (motif, date) {
        let eligibleBalanceList = []
        for (var motifIndex = 0; motifIndex < motif.length; motifIndex++) {
            var balancesElement = {};
            if (date <= moment(motif[motifIndex].dateFin).toDate() &&
                date >= moment(motif[motifIndex].dateDeb).toDate()) {
                balancesElement.longLabel = motif[motifIndex].reason.longLabel;
                balancesElement.duration = motif[motifIndex].remainder + '';
                balancesElement.dateFin = moment(motif[motifIndex].dateFin).format('DD/MM/YYYY');
                balancesElement.unitKey = motif[motifIndex].reason.unitKey;
                eligibleBalanceList.push(balancesElement);
            }
        }
        return eligibleBalanceList
    }

    /**
     * @description qtipUserInit : create the User popup
     * @param  {object} scheduler_treetimeline : dhtmlx scheduler
     * @param  {object} paidleaves : Pattern solde list
     *
     */

    var qtipUser = function(paidleaves, balanceList, date, id) {
        const motif = paidleaves?.balances?.[id]?.paidLeaves?.paidLeave;
        let eligibleBalanceList = getEligibleBalanceList(motif, date);
        if (eligibleBalanceList.length !== 0 && eligibleBalanceList.length !== balanceList.length) {
            balanceList.push(...eligibleBalanceList)
        }else {
            //We do nothing and balanceList stays the same because it has already been filled or there is no eligible motif
        }
        return balanceList.length !== 0
    };

    var qtipEvent = function(title, selectedUser, paidleaves, balanceList, date, id, e) {
        var event = e;
		if(_self.isMobile){
			content = {text: cockpit, show: 'click', button: 'Close'};
			position = {viewport: jquery(document.body), target: false, container: jquery(document.body), 
                adjust: {mouse: false, scroll: false, screen: true, resize: true}};
		}else{
			content = {text: cockpit, show: 'clik', button: 'Fermer', prerender: true};
			position = {viewport: jquery('#leaveplanning'), my: 'top left', at: 'center', target: jquery(event.target), container: jquery('.dhx_cal_data'),
				adjust: {method: 'flip shift', mouse: true, scroll: false, screen: true, resize: true}};
		}
        jquery(event.target).qtip({
            content: content,

            show: {
                event: 'click',
                ready: true,
                solo: true
            },
            hide: {
                event: hideOn,
                fixed: true
            },
            position: position,
            events: {
                show: function(ev, api) {

                    jquery('.qtip').qtip('hide');
                    var balanceNotEmpty = qtipUser(paidleaves, balanceList, date, id);
					if(_self.isMobile){
						clickType = 'touchstart click';
						jquery(ev.currentTarget).addClass("popup-leaveplanning");
					}else{
						clickType = 'click';
						jquery('.qtip').qtip('hide');
					}
                    var popupId = ev.currentTarget.id;
                    new Ractive({
                        el: jquery('#' + popupId + '-content #cockpit'),
                        template: popupUserContent,
                        data: {
                            title: title,
                            user: selectedUser,
                            balanceList: balanceList,
                            balanceNotEmpty: balanceNotEmpty
                        },
                        viewDetails: function(_id) {
                            var item = jquery('#' + popupId + '-content #cockpit #' + _id);

                            jquery(item).slideToggle(200, function() {
                                updateHeightWidget();
                                if (jquery(item).is(':visible')) {
                                    jquery('#open-arrow-' + _id).hide();
                                    jquery('#close-arrow-' + _id).show();
                                } else {
                                    jquery('#close-arrow-' + _id).hide();
                                    jquery('#open-arrow-' + _id).show();
                                }
                            });
                        }
                    });
                    jquery('.ui-icon.ui-icon-close')
                        .replaceWith('<svg aria-hidden="true" class="popupuser shrs-button__icon shrs-icon shrs-icon_size_medium"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#shrs-icon-cross"></use>');
                    _self.localizer.localize(jquery('#' + this[0].id + '-content #cockpit'));

                    jquery('#cancelBtn', api.elements.content).click(function() {
                        jquery('.qtip').qtip('hide');
                    });
                }
            }
        }).bind(clickType, function() {
            if (jquery('.bootstrap-datetimepicker-widget').length) {
                jquery('.input-group-addon').trigger(clickType);
            }
            e.stopPropagation();
            e.preventDefault();
			if(!_self.isMobile){
				return false;
			}
        });

    };

    leaveplanningCustomQtip.prototype.qtipUserInit = function(
        scheduler_treetimeline, paidleaves, _connectedUser) {
		if(_self.isMobile){
			clickType = 'touchstart click';
			eventParameter = '.dhx_matrix_scell.item:first';
		}else{
			clickType = 'click';
			eventParameter = '.zoom';
		}
        //popup content
        var title = '',
            selectedUser = {},
            balanceList = [],
            date = new Date();
        jquery('#leaveplanning .dhx_cal_data').on(clickType, eventParameter, function(e) {

            var obj = scheduler_treetimeline.getActionData(e);
            var _section = scheduler_treetimeline.getSection(obj.section);
            var section = _section.key;

            var id = _connectedUser.employeeInfoMap.SOCCLE.concat(_connectedUser.employeeInfoMap.MATCLE);
            var connectedSection = scheduler_treetimeline.getSection(section);

            selectedUser.name = connectedSection.name;
            selectedUser.quality = connectedSection.qualification;
            selectedUser.id = section;
            selectedUser.img = connectedSection.img;
            qtipEvent(title, selectedUser, paidleaves, balanceList, date, id, e);

        });
		     jquery('#leaveplanning').addClass('popup-user-initialized');
    };
    return leaveplanningCustomQtip;
});