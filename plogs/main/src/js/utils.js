(function () {
    "use strict";

    angular.module('plogsUtils', [])
        .constant('assetsRoot', '/static/assets')
        .factory('assets', function (assetsRoot) {
            return function (path) {
                return assetsRoot + "/" + path;
            };
        });
})();