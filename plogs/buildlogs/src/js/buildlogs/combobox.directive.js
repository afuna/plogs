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
            selectController.searchInput.on("keydown", function (e) {
                if (e.which == 13) {
                    e.preventDefault();
                    e.stopPropagation();
                }
            });
        }
    };
});
