var app = angular.module('buildlogDetail.controller', []);
app.controller('BuildLogDetailController', function BuildLogDetailController($routeParams, $location, BuildLog) {

    this.buildlog = {};

    BuildLog.get({
        username: $routeParams.username,
        project_id: $routeParams.project_id,
        log_id: $routeParams.log_id
    }).$promise
        .then(angular.bind(this, function then(data) {
            this.buildlog = data;
        }));

});