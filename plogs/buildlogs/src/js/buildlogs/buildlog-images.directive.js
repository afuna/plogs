var app = angular.module('buildlogImages.directive', []);
app.directive('buildlogImages', function BuildLogImagesDirective (buildlogsModuleAssets) {
    return {
        restrict: 'E',
        templateUrl: buildlogsModuleAssets('partials/buildlog-images.tmpl.html'),
        scope: {
            buildlog: '=',
        }
    };
});