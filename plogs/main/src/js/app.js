(function () {
    "use strict";

    angular.module('plogs', [
        'ngRoute',

        'plogsUtils',
        'index',
        'buildlogs'
    ])
    .config(function ($routeProvider, assetsRoot) {
        $routeProvider
            .when("/", {
                templateUrl: assetsRoot + '/buildlogs/views/frontpage.html',
                controller: 'IndexController',
                controllerAs: 'page'
            })
            .when("/people/:username/projects/:project_id/buildlogs", {
                templateUrl: assetsRoot + '/buildlogs/views/buildlogs-list.html',
                controller: 'BuildLogsController',
                controllerAs: 'page'
            })
            .when("/people/:username/projects/:project_id/buildlogs/:log_id", {

            })
            .otherwise({
                redirectTo: "/"
            });
    });
})();