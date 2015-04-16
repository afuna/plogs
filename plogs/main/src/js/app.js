(function () {
    "use strict";

    angular.module('plogs', [
        'ngRoute',

        'plogsUtils',
        'index',
        'logs'
    ])
    .config(function ($routeProvider, assetsRoot) {
        $routeProvider
            .when("/", {
                templateUrl: assetsRoot + '/buildlogs/views/frontpage.html',
                controller: 'IndexController',
                controllerAs: 'page'
            })
            .otherwise({
                redirectTo: "/"
            });
    });

})();