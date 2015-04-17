var app = angular.module('buildlogs.controller', []);
app.controller('BuildLogsController', function BuildLogsController($routeParams, $location, BuildLog, ActiveProjectFactory) {
    this.basePath = $location.path();

    BuildLog.query({
            username: $routeParams.username,
            project_id: $routeParams.project_id
    }).$promise
        .then(angular.bind(this, function then(data) {
            this.buildlogs = data.results;
            this.numBuildlogs = data.count;

            ActiveProjectFactory.getProject()
                .then(angular.bind(this, function then(data) {
                    this.project = data;
                }));
        }));
});