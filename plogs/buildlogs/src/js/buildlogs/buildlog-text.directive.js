var app = angular.module('buildlogText.directive', ['ngSanitize']);
app.directive('buildlogText', function BuildLogTextDirective(buildlogsModuleAssets) {
    return {
        restrict: 'E',
        templateUrl: buildlogsModuleAssets('partials/buildlog-text.tmpl.html'),
        scope: {
            buildlog: '='
        },
        controllerAs: "buildlogTextController",
        controller: function BuildLogTextController($scope, $sce) {
            // this has been cleaned for us by django
            // so trust it
            this.cleanedNote = function () {
                return $sce.trustAsHtml($scope.buildlog.notes);
            };
        }
    };
});