/********************************************************

 * @description :  The "leaveplanning date time picker"

 ********************************************************/
require(['css!/resources/js/lib/bootstrap-datetimepicker/bootstrap-datetimepicker.min']);
define('@{mvn:widget.web.context.path}/leaveplanningDatePicker.js', function(require) {
    'use strict';
    var moment = require('moment'),
        bsdatetime = require('bsdatetime'), // NOSONAR
        localizer, tooltipconfig,
        jquery = require('jquery');

    var leaveplanningDatePicker = function(_localizer) {
        localizer = _localizer;

        try {
            tooltipconfig = {
                "today": localizer.getText('today'),
                "clear": localizer.getText('clear'),
                "close": localizer.getText('close'),
                "selectMonth": localizer.getText('selectMonth'),
                "prevMonth": localizer.getText('prevMonth'),
                "nextMonth": localizer.getText('nextMonth'),
                "selectYear": localizer.getText('leaveplanning_selectYear'),
                "nextYear": localizer.getText('leaveplanning_nextYear'),
                "prevYear": localizer.getText('leaveplanning_prevYear'),
                "selectDecade": localizer.getText('selectDecade'),
                "prevDecade": localizer.getText('prevDecade'),
                "nextDecade": localizer.getText('nextDecade'),
                "prevCentury": localizer.getText('prevCentury'),
                "nextCentury": localizer.getText('nextCentury')
            }
        } catch (error) {
            logger.error(error);
        }
    };
    /**
     * @public configuration of the dateTimePicker
     * @returns {undefined}
     */
    leaveplanningDatePicker.prototype.setDateTimePickerConfiguration = function(
        leaveplanning_treetimeline) {
        jquery('#date_now').on('click', function() {
            jquery('.input-group-addon').trigger('click');
        });
        // init date-piker & change scheduler view to current date
        jquery('#planning_datetimepicker').datetimepicker({
            viewMode: 'months',
            format: 'MM/YYYY',
            useCurrent: false,
            minDate: moment().add(-1, 'years').startOf('year'),
            maxDate: moment().add(1, 'years').endOf('year'),
            tooltips: tooltipconfig
        }).on('dp.change', function(e) {
            jquery("div[id*='qtip']").hide();
            // set scheduler to selected date
            if (jquery('.bootstrap-datetimepicker-widget').length !== 0) {
                var selectedDate = e.date._d;
                leaveplanning_treetimeline.setCurrentView(selectedDate);
                // refresh date now text
                jquery('#date_now').empty();
                var month = moment(e.date._d).format('MMMM');
                jquery('#date_now').append(month + ' ' + e.date._d.getFullYear());
            }
        });
        jquery('#planning_datetimepicker').click(function() {
            jquery('.bootstrap-datetimepicker-widget.dropdown-menu.bottom').css({
                'top': '30px'
            });
        });
        jquery('#header-menu-bar').click(function() {
            if (jquery('.bootstrap-datetimepicker-widget').length) {
                jquery('.input-group-addon').trigger('click');
            }
        });
        leaveplanning_treetimeline.attachEvent('onCellClick', function() {
            if (jquery('.bootstrap-datetimepicker-widget').length) {
                jquery('.input-group-addon').trigger('click');
            }
        });
        leaveplanning_treetimeline.attachEvent('onEmptyClick', function() {
            if (jquery('.bootstrap-datetimepicker-widget').length) {
                jquery('.input-group-addon').trigger('click');
            }
        });
        leaveplanning_treetimeline.attachEvent('onSelect', function() {
            if (jquery('.bootstrap-datetimepicker-widget').length) {
                jquery('.input-group-addon').trigger('click');
            }
        });
    };
    return leaveplanningDatePicker;
});