var app = angular.module('index', [
    'index.controller',
    'index.active-project.factory',
    'index.stats.directive',
    'plogsUtils'
])
.factory('indexModuleAssets', function (assets) {
    return function (path) {
        return assets("buildlogs/js/index/" + path);
    };
});
