var app = angular.module('index.stats.directive', []);
app.directive('stats', function (indexModuleAssets) {
    return {
        restrict: 'E',
        scope: {
            project: "="
        },
        templateUrl: indexModuleAssets('partials/stats.tmpl.html'),
        controllerAs: 'projectInfo',
        controller: function($scope,ProjectFactory) {
            this.stats = {"hours": 0, "dollars": 0, "sessions": 0};

            ProjectFactory.getStats()
                .then(angular.bind(this, function then(data) {
                    this.stats = data;
                }));
        }
    };
});
