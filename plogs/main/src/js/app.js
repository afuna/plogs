(function () {
    "use strict";

    angular.module('plogs', [
        'ngRoute',

        'plogsUtils',
        'auth',
        'index',
        'buildlogs',
        'breadcrumbs'
    ])
    .config(function ($routeProvider, assetsRoot) {
        var buildlogsPath = '/people/:username/projects/:project_id/buildlogs'
        $routeProvider
            .when("/", {
                templateUrl: assetsRoot + '/main/views/index.html',
                controller: 'IndexController',
                controllerAs: 'page'
            })
            .when(buildlogsPath, {
                templateUrl: assetsRoot + '/buildlogs/views/buildlogs-list.html',
                controller: 'BuildLogsController',
                controllerAs: 'page'
            })
            .when(buildlogsPath + '/new', {
                templateUrl: assetsRoot + '/buildlogs/views/buildlogs-form.html'
            })
            .when(buildlogsPath + '/:log_id', {
                templateUrl: assetsRoot + '/buildlogs/views/buildlogs-detail.html',
                controller: 'BuildLogDetailController',
                controllerAs: 'page'
            })
            .otherwise({
                redirectTo: "/"
            });
    })
    .config(function ($httpProvider) {
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.headers.post["X-Requested-With"] = "XMLHttpRequest";
    });
})();