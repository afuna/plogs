var app = angular.module('index.controller', []);
app.controller('IndexController', function (ActiveProjectFactory) {
    this.project = ActiveProjectFactory.stubProject();

    ActiveProjectFactory.getProjectStats()
        .then(angular.bind(this, function then(data) {
            this.project = data;
        }));
});
