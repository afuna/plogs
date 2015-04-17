var app = angular.module('buildlogMetadata.directive', []);
app.directive('buildlogMetadata', function BuildLogMetadataDirective(buildlogsModuleAssets) {
    return {
        restrict: 'E',
        templateUrl: buildlogsModuleAssets('partials/buildlog-metadata.tmpl.html'),
        scope: {
            buildlog: '='
        },
        controller: function ($scope) {
            // transform the buildlog metadata into an easily iterable array
            $scope.$watch('buildlog', function () {
                var buildlog = $scope.buildlog,
                    metadata = [];

                if (buildlog.category) {
                    metadata.push(["Category", buildlog.category]);
                }

                if (buildlog.partner) {
                    metadata.push(["Partner", buildlog.partner]);
                }

                if (buildlog.duration) {
                    metadata.push(["Hours", buildlog.duration]);
                }

                if (buildlog.reference) {
                    metadata.push(["Reference", buildlog.reference]);
                }

                if (buildlog.parts) {
                    metadata.push(["Parts", buildlog.parts]);
                }

                $scope.metadata = metadata;
            });
        }
    };
});