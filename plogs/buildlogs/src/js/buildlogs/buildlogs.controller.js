var app = angular.module('buildlogs.controller', []);
app.controller('BuildLogsController', function BuildLogsController($routeParams, $location, BuildLog, ActiveProjectFactory) {
    this.basePath = $location.path();
    this.buildlogs = [];

    var currentPage = 1;
    var loadBuildLogs = angular.bind(this, function(page_number) {
        BuildLog.query({
                username: $routeParams.username,
                project_id: $routeParams.project_id,
                page: page_number
        }).$promise
            .then(angular.bind(this, function then(data) {
                this.buildlogs = this.buildlogs.concat(data.results);
                this.numBuildlogs = data.count;
                this.hasMore = this.buildlogs.length < this.numBuildlogs;

                ActiveProjectFactory.getProject()
                    .then(angular.bind(this, function then(data) {
                        this.project = data;
                    }));
            }));
    });

    this.loadMore = function () {
        currentPage += 1;
        loadBuildLogs(currentPage);
    };

    loadBuildLogs(currentPage);
});