var app = angular.module('buildlogs', [
    'buildlogs.factory',
    'buildlogs.controller',
    'plogsUtils'
])
.factory('logModuleAssets', function (assets) {
    return function (path) {
        return assets("buildlogs/js/logs/" + path);
    };
});