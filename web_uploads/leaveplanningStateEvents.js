/************************************************

 * @description :  The "leaveplanning events"

 ***********************************************/

define('@{mvn:widget.web.context.path}/leaveplanningStateEvents.js',
    function(require) {
        'use strict';
        const
            arrowIconOpened =
            '<svg aria-hidden="true" class="shrs-button__icon shrs-icon shrs-icon_size_small" style="pointer-events: none;">' +
            '<use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#shrs-icon-triangle-bottom"></use>"></svg>',
            arrowIconClosed =
            '<svg aria-hidden="true" class="shrs-button__icon shrs-icon shrs-icon_size_small" style="pointer-events: none;">' +
            '<use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#shrs-icon-triangle-right"></use>"></svg>';

        var jquery = require('jquery');
        var moment = require('moment');
		var firstClick =  false;
		var _that;
		const HEIGHT_ROW = 52;
		var intervalUpdateHeight = null;
		var newHeightValue = 0;
        /**
         * @Constructor
         */
        var leaveplanningStateEvents = function(_isMobile) {
			this.isMobile = _isMobile;
			_that = this;
			if(_that.isMobile){
				firstClick = true;
			}
        };
		
        var checkScreenSize = function (matrixTimeline, days, date, old_date) {
            //all devices except tabvar
            if (device.tablet() === false) {
                matrixTimeline.x_size = days;
                matrixTimeline.x_length = days;
				
            } else {//tabvar
				var newTimeline = getTabletTimelineData (date);
				matrixTimeline.x_size = newTimeline.size;
				matrixTimeline.x_start = newTimeline.start;
                matrixTimeline.x_length = matrixTimeline.x_size;			
			}
			if(_that.isMobile){
				if (days === 31) {
					matrixTimeline.dx = 62;
				}
				else if (days === 30) {
					matrixTimeline.dx = 81;
				}
				else if (days === 28) {
					matrixTimeline.dx = 71;
				}
			}
		};

        var onEventLoading = function(leaveplanning_scheduler) {
            leaveplanning_scheduler.attachEvent('onEventLoading', function(ev) {
                return leaveplanning_scheduler.checkCollision(ev);
            });
        };
		
        /**
         * @description  Called on scheduler init to set date
         */
        var onTemplatesReady = function(leaveplanning_scheduler) {
            leaveplanning_scheduler.attachEvent('onTemplatesReady', function() {
                var date = new Date();
                var month = moment(date).format('MMMM');
                jquery('#date_now').append(month + ' ' + date.getFullYear());
                jquery('#leaveplanning').show();
                leaveplanning_scheduler.templates.event_text = function(
                    start, end, ev) {
                    return ev.text;
                };
            });
        };
        /**
         * @description  Called to customize the timeline sections with arrow indicator for section tree
         */
        var onBeforeSectionRender = function(leaveplanning_scheduler) {
            leaveplanning_scheduler.attachEvent('onBeforeSectionRender', function(render_name, y_unit, timeline) {
                var res = {};
                var height;
                // section 1
                var tr_className, style_height, td_className;
                var div_expand;
                // section 3
                var table_className;
                if (render_name === 'tree') {
                    if (y_unit.children) {
                        height = timeline.folder_dy || timeline.dy;
                        if (timeline.folder_dy && !timeline.section_autoheight) {
                            style_height = 'height:' + timeline.folder_dy + 'px;';
                        }
                        tr_className = 'dhx_row_folder';
                        td_className = 'dhx_matrix_scell folder' +
                            (y_unit.delegated === true ? ' delegatedTeam' : '');
                        jquery('.shrs-button__icon').children().unbind('click');
                        div_expand = '<div class="dhx_scell_expand">' +
                            ((y_unit.open) ? arrowIconOpened : arrowIconClosed) +
                            '</div>';
                        table_className = (timeline.folder_events_available) ? 'dhx_data_table folder_events' :
                            'dhx_data_table folder';
                    } else {
                        if (y_unit.role === 'manager') {
                            height = HEIGHT_ROW;
                            tr_className = 'dhx_row_item ' + y_unit.key + ' manager_cell';
                            td_className = 'dhx_matrix_scell item  ' +
                                y_unit.key +
                                (leaveplanning_scheduler.templates[timeline.name + '_scaley_class'](y_unit.key,
                                        y_unit.label, y_unit) ? ' ' +
                                    leaveplanning_scheduler.templates[timeline.name + '_scaley_class'](y_unit.key,
                                        y_unit.label, y_unit) : '');
                            div_expand = '';
                            table_className = 'dhx_data_table';
                        } else
                        if (y_unit.role === 'height_adjust') {
                            height = timeline.dy;
                            tr_className = 'dhx_row_item height_adjust  ' + y_unit.key;
                            td_className = 'dhx_matrix_scell item ' +
                                y_unit.key +
                                (leaveplanning_scheduler.templates[timeline.name + '_scaley_class'](y_unit.key,
                                        y_unit.label, y_unit) ? ' ' +
                                    leaveplanning_scheduler.templates[timeline.name + '_scaley_class'](y_unit.key,
                                        y_unit.label, y_unit) : '');
                            div_expand = '';
                            table_className = 'dhx_data_table';
                        } else {
                            height = HEIGHT_ROW;
                            tr_className = 'dhx_row_item ' + y_unit.key;
                            td_className = 'dhx_matrix_scell item ' +
                                y_unit.key +
                                (leaveplanning_scheduler.templates[timeline.name + '_scaley_class'](y_unit.key,
                                        y_unit.label, y_unit) ? " " +
                                    leaveplanning_scheduler.templates[timeline.name + '_scaley_class'](y_unit.key,
                                        y_unit.label, y_unit) : '');
                            div_expand = '';
                            table_className = 'dhx_data_table';
                        }
                    }
                }
                var delegatedContent = y_unit.delegated === true ? '<span class="delegated_team_text">' +
                    localizer.getText('delegatedTeamLabel') + '</span>' : '';
                var td_content = '<div class="dhx_scell_level"' +
                    y_unit.level +
                    '">' +
                    div_expand +
                    '<div class="dhx_scell_name">' +
                    (leaveplanning_scheduler.templates[timeline.name + '_scale_label'](y_unit.key, y_unit.label,
                        y_unit) || y_unit.label) + '' + delegatedContent + '</div></div>';
                res = {
                    height: height,
                    style_height: style_height,
                    // section 1
                    tr_className: tr_className,
                    td_className: td_className,
                    td_content: td_content,
                    // section 3
                    table_className: table_className
                };
                return res;
            });
        };

        /**
         * @description  Called when scheduler is initially being rendered or before user changes to a new view
         */
        var onBeforeViewChange = function(leaveplanning_scheduler, employee) {

            leaveplanning_scheduler.attachEvent('onBeforeViewChange', function(old_mode, old_date, mode, date) {
                var year = date.getFullYear();
                var month = (date.getMonth() + 1);
                var currentViewDate = new Date(year, month, 0);
                //gets all events of the scheduler
                var days = currentViewDate.getDate();
                var matrixTimeline = leaveplanning_scheduler.matrix.timeline;
                // scroll_width //IE navigator.userAgent.match(/Trident/)
                var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
				if(_that.isMobile){
					jquery(".dhx_cal_data")[0].scrollLeft = 0;
					if(firstClick && jquery("#scheduler_here .dhx_cal_data .dhx_cal_event_line").length > 0){
						firstClick = false;
						jquery("#scheduler_here .dhx_cal_data .dhx_cal_event_line")[0].click();
					}
				}
                if (isChrome) {
                    leaveplanning_scheduler.xy.scroll_width = 10;
                } else {
                    // if other browser
                    leaveplanning_scheduler.xy.scroll_width = 20;
                }
                checkScreenSize(matrixTimeline, days, date, old_date);
				
                //show leave label on hover
                setTimeout(function() {
                    var evs = leaveplanning_scheduler.getEvents();
                    if (evs.length === 0) {
                        return;
                    }
                    var employeeindex = _.findIndex(evs, function(e) {
                        return e.section_id.indexOf(employee) > -1;
                    });
                    if (employeeindex === -1) {
                        return;
                    }
                    var section_id = evs[employeeindex].section_id.replace(/[&\/\\#,+()$~%.'":*?<>{}]/g, '');
                    _.forEach(jquery('.' + section_id).find('.dhx_cal_event_line'), function(elt) {
                        var element = jquery(elt);
                        var index = _.findIndex(evs, function(e) {
                            return e.id === Number(element.attr('event_id'));
                        });
                        element.attr('title', evs[index].longLabel || evs[index].label);
                    });
                }, 1000);


                return true;
            });
        };
        var onSchedulerResize = function(leaveplanning_scheduler) {
            leaveplanning_scheduler.attachEvent('onSchedulerResize', function() {
                // hide datepicker
                if (jquery('.bootstrap-datetimepicker-widget').length) {
                    jquery('.input-group-addon').trigger('click');
                }
				if(_that.isMobile){
					var dates = jquery('.dhx_cal_date').text();
					var dates_array = dates.split(' - ');
					var startDate = moment(dates_array[0], 'D MMM YYYY').get('date');
					var endDate = moment(dates_array[1], 'D MMM YYYY').get('date');
					jquery('.dhx_cal_date').text(startDate + " - " + endDate);
				}
            });
        };

        /**
         * @description  Called when current view is changed
         */
        var onViewChange = function(leaveplanning_scheduler, refreshPlanning) {
            leaveplanning_scheduler.attachEvent('onViewChange', function(new_mode, new_date) {
                // hide datepicker
                if (jquery('.bootstrap-datetimepicker-widget').length) {
                    jquery('.input-group-addon').trigger('click');
                }
                // refresh date now text
                jquery('#date_now').empty();
                var _new_date = new_date;
				var printMonth = moment(_new_date).format('MMMM');
				if(_that.isMobile){
					printMonth = moment(_new_date).add(1, 'days').format('MMMM');
				}
				jquery('#planning_datetimepicker').data("DateTimePicker").date(new_date);
				jquery('#date_now').append(printMonth + ' ' + _new_date.getFullYear());
				
				// disable btn month nav
                var dhx_cal_next_button = '.dhx_cal_next_button';
                if (moment(new_date).endOf('month').format('DD/MM/YYYY') === moment()
                    .add(1, 'years').endOf('year')
                    .format('DD/MM/YYYY')) {
                    jquery(dhx_cal_next_button).addClass('btn_disable');
                    jquery(dhx_cal_next_button).children().unbind('click');
                } else {
                    jquery(dhx_cal_next_button).children().bind('click');
                    jquery(dhx_cal_next_button).removeClass('btn_disable');
                }
                var dhx_cal_prev_button = '.dhx_cal_prev_button';
                if (moment(new_date).format('MM/YYYY') === moment()
                    .add(-1, 'years').startOf('year').format('MM/YYYY')) {
                    jquery(dhx_cal_prev_button).addClass('btn_disable');
                    jquery(dhx_cal_prev_button).children().unbind('click');
                } else {
                    jquery(dhx_cal_prev_button).children().bind('click');
                    jquery(dhx_cal_prev_button).removeClass('btn_disable');
                }
                // hide date interval for PC
                jquery('.dhx_cal_date').hide();

				var temporaryDate = moment(new_date).format('YYYY-MM-DD');
				var start = moment().add(-1, 'month').startOf('month').format('YYYY-MM-DD');
				var end = moment().add(1, 'month').endOf('month').format('YYYY-MM-DD');
				var loadThreeMonths = temporaryDate >= start &&  temporaryDate <= end;
				if(loadThreeMonths === false){
					refreshPlanning(new_date);
				}
				updateHeightCalData();
            });
        };

        // Set the real Height of cal Data
        function updateHeightCalData() {
            if ( intervalUpdateHeight ){
                clearInterval(intervalUpdateHeight)
            }
            if ( ! _that.isMobile ){
                intervalUpdateHeight = setInterval(function(){
                    var $dhxCalData = jquery('#leaveplanning .dhx_cal_data');
                    if ( $dhxCalData.length > 0  ){
                        const ADDONS  = 5;
                        var height = $dhxCalData.height();
                        if ( newHeightValue !== height){
                            var newHeight = $dhxCalData.position().top - HEIGHT_ROW +  ADDONS;
                            var oldStyle= $dhxCalData.attr('style');
                            $dhxCalData.css('height', '');
                            $dhxCalData.attr('style', oldStyle + 'height: calc(100% - ' + newHeight  + 'px) !important;');
                            newHeightValue = $dhxCalData.height();
                        }
                    }else{
                        clearInterval(intervalUpdateHeight)
                    }
                }, 300)
            }
        }

        function getCellClassForClassicEventPositionOfLeaveValidatedWithoutJustif(start, end, minDate, maxDate) {
            if (start < minDate && end > minDate && start < maxDate && end < maxDate) {
                return 'validated_waiting_justif_vcell_end';
            } else if (start > minDate && end > minDate && start < maxDate && end > maxDate) {
                return 'validated_waiting_justif_vcell_start';
            } else if (end > minDate && start < maxDate && end > maxDate) {
                return 'validated_waiting_justif_vcell_start';
            } else if (start > minDate && end > minDate && start < maxDate && end > maxDate) {
                return 'validated_waiting_justif_vcell';
            } else if (end > minDate && start < maxDate && end < maxDate) {
                return 'validated_waiting_justif_vcell';
            } else {
                return 'validated_waiting_justif_vcell_open';
            }
        }

        function getCellClassForOwnLeaveValidatedWithoutJustif(start, end, event, minDate, maxDate) {
            if (event.position === 'start') {
                return 'validated_waiting_justif_vcell_start';

            } else if (event.position === 'end') {
                if (start <= minDate && end > minDate && start < maxDate && end <= maxDate) {
                    return 'validated_waiting_justif_vcell_end';
                } else if (start >= minDate && end > minDate && start < maxDate && end >= maxDate) {
                    return 'validated_waiting_justif_vcell_open';
                } else if (start >= minDate && end > minDate && start < maxDate && end >= maxDate) {
                    return 'validated_waiting_justif_vcell';
                } else {
                    return 'validated_waiting_justif_vcell_end';
                }

            } else if (event.position === 'middle') {
                return 'validated_waiting_justif_vcell_open';

            } else if (event.position === 'classic') {
                return getCellClassForClassicEventPositionOfLeaveValidatedWithoutJustif(start, end, minDate, maxDate);
            }
        }

        var event_class = function(employee, leaveplanning_scheduler) {
            leaveplanning_scheduler.templates.event_class = function(start, end, event) {
                var minDate = leaveplanning_scheduler.getState().min_date;
                var maxDate = leaveplanning_scheduler.getState().max_date;
                // to validate
                if (event.customType === 'tovalidate' && event.section_id.indexOf(employee) !== -1) {
                    if (event.position === 'start') {
                        return 'to_validate_vcell_start';
                    }
                    if (event.position === 'end') {
                        if (start <= minDate && end > minDate && start < maxDate && end <= maxDate) {
                            return 'to_validate_vcell_end';
                        }
                        if (start >= minDate && end > minDate && start < maxDate && end >= maxDate) {
                            return 'to_validate_vcell_open';
                        }
                        if (start >= minDate && end > minDate && start < maxDate && end >= maxDate) {
                            return 'to_validate_vcell';
                        }
                        return 'to_validate_vcell_end';
                    }
                    if (event.position === 'middle') {
                        return 'to_validate_vcell_open';
                    }
                    if (event.position === 'classic') {
                        if (start < minDate && end > minDate && start < maxDate && end < maxDate) {
                            return 'to_validate_vcell_end';
                        }
                        if (start > minDate && end > minDate && start < maxDate && end > maxDate) {
                            return 'to_validate_vcell_start';
                        }
                        if (end > minDate && start < maxDate && end > maxDate) {
                            return 'to_validate_vcell_start';
                        }
                        if (start > minDate && end > minDate && start < maxDate && end > maxDate) {
                            return 'to_validate_vcell';
                        }
                        if (end > minDate && start < maxDate && end < maxDate) {
                            return 'to_validate_vcell';
                        }
                        return 'to_validate_vcell_open';
                    }
                }

                // period validated waiting for justif 
                if (event.customType === 'justifToValidate' && event.section_id.indexOf(employee) !== -1) {
                    return getCellClassForOwnLeaveValidatedWithoutJustif(start, end, event, minDate, maxDate);
                }
                // cancellationRequest
                else if (event.section_id.indexOf(employee) !== -1 && event.customType === 'cancellationRequest') {
                    if (start < minDate && end > minDate && start < maxDate && end < maxDate) {
                        return 'cancellation_Request_vcell_end';
                    }
                    if (start > minDate && end > minDate && start < maxDate && end < maxDate) {
                        return 'cancellation_Request_vcell';
                    }
                    if (start > minDate && end > minDate && start < maxDate && end > maxDate) {
                        return 'cancellation_Request_vcell_start';
                    }
                    if (end > minDate && start < maxDate && end > maxDate) {
                        return 'cancellation_Request_vcell_start';
                    }
                    if (start > minDate && end > minDate && start < maxDate && end > maxDate) {
                        return 'cancellation_Request_vcell';
                    }
                    if (end > minDate && start < maxDate && end < maxDate) {
                        return 'cancellation_Request_vcell';
                    }
                    return 'cancellation_Request_vcell';
                }

                // Draft abscence
                else if (event.section_id.indexOf(employee) !== -1 && event.customType === 'draft') {
                    if (start < minDate && end > minDate && start < maxDate && end < maxDate) {
                        return 'draft_vcell_end';
                    }
                    if (start > minDate && end > minDate && start < maxDate && end < maxDate) {
                        return 'draft_vcell';
                    }
                    if (start > minDate && end > minDate && start < maxDate && end > maxDate) {
                        return 'draft_vcell_start';
                    }
                    if (end > minDate && start < maxDate && end > maxDate) {
                        return 'draft_vcell_start';
                    }
                    if (start > minDate && end > minDate && start < maxDate && end > maxDate) {
                        return 'draft_vcell';
                    }
                    if (end > minDate && start < maxDate && end < maxDate) {
                        return 'draft_vcell';
                    }
                    return 'draft_vcell';
                }
                // To validatetasks of my collegue //
                else if ((event.customType === 'tovalidatetasks') || (event.customType === 'tovalidate')) {
                    if (start < minDate && end > minDate &&
                        start < maxDate && end < maxDate) {
                        return 'to_validate_vcell_end';
                    }
                    if (start > minDate && end > minDate &&
                        start < maxDate && end > maxDate) {
                        return 'to_validate_vcell_start';
                    }
                    if (end > minDate && start < maxDate &&
                        end > maxDate) {
                        return 'to_validate_vcell_start';
                    }
                    if (start > minDate && end > minDate &&
                        start < maxDate && end > maxDate) {
                        return 'to_validate_vcell';
                    }
                    if (end > minDate && start < maxDate &&
                        end < maxDate) {
                        return 'to_validate_vcell';
                    }
                    return 'to_validate_vcell_open';
                }
                // Justif to validate of my collegue //
                else if (event.customType === 'justifToValidate') {
                    return getCellClassForClassicEventPositionOfLeaveValidatedWithoutJustif(start, end, minDate, maxDate);
                }
                // cancellationRequesttasks of my collegue //
                else if ((event.customType === 'cancellationRequesttasks') || (event.customType === 'cancellationRequest')) {
                    if (start < minDate && end > minDate &&
                        start < maxDate && end < maxDate) {
                        return 'cancellation_Request_vcell_end';
                    }
                    if (start > minDate && end > minDate &&
                        start < maxDate && end > maxDate) {
                        return 'cancellation_Request_vcell_start';
                    }
                    if (end > minDate && start < maxDate &&
                        end > maxDate) {
                        return 'cancellation_Request_vcell_start';
                    }
                    if (start > minDate && end > minDate &&
                        start < maxDate && end > maxDate) {
                        return 'cancellation_Request_vcell';
                    }
                    if (end > minDate && start < maxDate &&
                        end < maxDate) {
                        return 'cancellation_Request_vcell';
                    }
                    return 'cancellation_Request_vcell_open';
                }
                // handle validated absences Other_Absences/Paid_Vacation
                else if (event.customType === 'validated') {
                    let className = '';
                    if(event.type === 'telework') {
                        className = 'telework ';
                    }
                    if (start < minDate && end > minDate &&
                        start < maxDate && end < maxDate) {
                        return className + 'validated_vcell_end ';
                    }
                    if (start > minDate && end > minDate &&
                        start < maxDate && end > maxDate) {
                        return className + 'validated_vcell_start ';
                    }
                    if (end > minDate && start < maxDate &&
                        end > maxDate) {
                        return className + 'validated_vcell_start ';
                    }
                    if (start > minDate && end > minDate &&
                        start < maxDate && end > maxDate) {
                        return className + 'validated_vcell ';
                    }
                    if (end > minDate && start < maxDate &&
                        end < maxDate) {
                        return className + 'validated_vcell ';
                    }
                    return className + 'validated_vcell_open ';
                }
            }
        };

        leaveplanningStateEvents.prototype.events = function(employee, leaveplanning_scheduler, localizer, refreshPlanning) {

            onEventLoading(leaveplanning_scheduler);
            onTemplatesReady(leaveplanning_scheduler);
            onBeforeSectionRender(leaveplanning_scheduler);
            onBeforeViewChange(leaveplanning_scheduler, employee);
            onSchedulerResize(leaveplanning_scheduler);
            onViewChange(leaveplanning_scheduler, refreshPlanning);
            event_class(employee, leaveplanning_scheduler);

        };

        function getTabletPeriodSize (date) {
            var newTimeline = getTabletTimelineData(date);
            return newTimeline.size;
        }
        leaveplanningStateEvents.getTabletPeriodSize = getTabletPeriodSize;

        function getTabletTimelineData (date) {
            var dateDay = moment(date).date();
            var monthDays = moment(date).daysInMonth();
            var firstPeriodDays = Math.floor(monthDays / 2);
            if (dateDay <= firstPeriodDays) {
                return {
                    size: firstPeriodDays,
                    start: 1 - dateDay
                };
            } else {
                return {
                    size: monthDays - firstPeriodDays,
                    start: firstPeriodDays + 1 - dateDay
                };
            }
        }
		
        return leaveplanningStateEvents;
    });
