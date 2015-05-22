/*
Combobox directive extends ui-select.

Additional behaviors:

    * Prevent form submit when you hit "enter" while entering a new item

*/
var app = angular.module('combobox.directive', [
    'mgcrea.ngStrap.datepicker',
    'ngSanitize',
    'ui.select'
]);
app.directive('combobox', function () {
    return {
        require: '^uiSelect',
        link: function(scope, element, attrs, selectController) {
            var select = selectController.select;
            selectController.select = function(item, skipFocusser, $event) {
                // we want to handle new items ourselves, not using the default
                // (especially for TAB)
                if (item === undefined) return;
                select(item, skipFocusser, $event);
            }

            selectController.searchInput.on("keydown", function (e) {
                if (e.which == 13) {
                    e.preventDefault();
                    e.stopPropagation();
                } else if (e.which == 9) {
                    if (selectController.activeIndex == -1) {
                        selectController.activate(false, true);
                    }
                }
            });
        }
    };
});
