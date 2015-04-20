var app = angular.module('index.controller', []);
app.controller('IndexController', function (ActiveProjectFactory, AuthenticationFactory) {
    this.project = ActiveProjectFactory.stubProject();

    AuthenticationFactory.isAuthenticated()
        .then(angular.bind(this, function then(data) {
            if (data.authenticated) {
                this.auth_logged_in = true;
            } else {
                this.auth_logged_out = true;
            }
        }));

    ActiveProjectFactory.getProjectStats()
        .then(angular.bind(this, function then(data) {
            this.project = data;
        }));
});
