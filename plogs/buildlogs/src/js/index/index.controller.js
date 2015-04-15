var app = angular.module('index.controller', []);
app.controller('IndexController', function (ProjectFactory) {
    ProjectFactory.getProject()
        .then(angular.bind(this, function then(data) {
            this.project = data;
        }));
});
