var app = angular.module('buildlogDetail.controller', []);
app.controller('BuildLogDetailController', function BuildLogDetailController($routeParams, $location, BuildLog, AuthenticationFactory) {

    this.buildlog = {};

    BuildLog.get({
        username: $routeParams.username,
        project_id: $routeParams.project_id,
        log_id: $routeParams.log_id
    }).$promise
        .then(angular.bind(this, function then(data) {
            this.buildlog = data;

            AuthenticationFactory.isAuthenticated()
                .then(angular.bind(this, function then(data) {
                    if (data.authenticated) {
                        this.buildlog.edit_url = "#" + $location.path()+"/edit";
                    }
                })
            );
        }));
});