var app = angular.module('buildlogTitle.directive', []);
app.directive('buildlogTitle', function BuildLogTitleDirective(buildlogsModuleAssets) {
    return {
        restrict: 'E',
        templateUrl: buildlogsModuleAssets('partials/buildlog-title.tmpl.html'),
        scope: {
            buildlog: '='
        }
    };
});