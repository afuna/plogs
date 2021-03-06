var app = angular.module('buildlogs.controller', []);
app.controller('BuildLogsController', function BuildLogsController($routeParams, $location, BuildLog, ProjectFactory) {
    this.basePath = $location.path();
    this.buildlogs = [];
    this.numBuildlogs = 0;

    var currentPage = 1;
    var loadBuildLogs = angular.bind(this, function loadBuildLogs(page_number) {
        BuildLog.query({
            username: $routeParams.username,
            project: $routeParams.project,
            page: page_number
        }).$promise
            .then(angular.bind(this, function then(data) {
                this.buildlogs = this.buildlogs.concat(data.results);
                this.numBuildlogs = data.count;
                this.hasMore = this.buildlogs.length < this.numBuildlogs;
            }));

        ProjectFactory.getProject($routeParams.username, $routeParams.project)
            .then(angular.bind(this, function then(data) {
                this.project = data;
            }));
    });

    this.loadMore = function () {
        currentPage += 1;
        loadBuildLogs(currentPage);
    };

    loadBuildLogs(currentPage);
});