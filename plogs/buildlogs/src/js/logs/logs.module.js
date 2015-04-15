(function () {
    "use strict";

    var app = angular.module('logs', [
        'plogsUtils'
    ])
    .factory('logModuleAssets', function (assets) {
        return function (path) {
            return assets("buildlogs/js/logs/" + path);
        };
    });
})();