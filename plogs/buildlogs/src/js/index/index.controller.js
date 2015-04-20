var app = angular.module('index.controller', []);
app.controller('IndexController', function (ProjectFactory, AuthenticationFactory) {
    this.project = ProjectFactory.stubProject();

    AuthenticationFactory.isAuthenticated()
        .then(angular.bind(this, function then(data) {
            if (data.authenticated) {
                this.auth_logged_in = true;
            } else {
                this.auth_logged_out = true;
            }
        }));

    ProjectFactory.getActiveProject()
        .then(angular.bind(this, function then(data) {
            this.project = data;
        }));
});
