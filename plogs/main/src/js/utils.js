(function () {
    "use strict";

    angular.module('plogsUtils', [])
        .constant('assetsRoot', '/static/assets')
        .factory('assets', function (assetsRoot, $location) {
            return function (path) {
                var cachebuster = "";
                if ($location.search()['debug']) {
                    cachebuster = "?v=" + (new Date()).getTime();
                }
                return assetsRoot + "/" + path + cachebuster;
            };
        });
})();