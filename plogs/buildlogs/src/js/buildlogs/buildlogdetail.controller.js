var app = angular.module('buildlogDetail.controller', []);
app.controller('BuildLogDetailController', function BuildLogDetailController($routeParams, $location, BuildLog, AuthenticationFactory) {

    this.buildlog = {};

    BuildLog.get({
        username: $routeParams.username,
        project: $routeParams.project,
        log_id: $routeParams.log_id
    }).$promise
        .then(angular.bind(this, function then(data) {
            if (data.parts) {
                data.parts = data.parts.join(", ");
            }

            if (data.reference) {
                data.reference = data.reference.join(", ");
            }

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