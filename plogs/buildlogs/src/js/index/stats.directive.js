var app = angular.module('index.stats.directive', []);
app.directive('stats', function (indexModuleAssets) {
    return {
        restrict: 'E',
        templateUrl: indexModuleAssets('partials/stats.tmpl.html'),
        scope: {
            project: "="
        },
        controllerAs: 'stats'
    };
});
