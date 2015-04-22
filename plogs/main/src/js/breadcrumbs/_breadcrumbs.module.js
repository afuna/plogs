var app = angular.module('breadcrumbs', [
    'breadcrumbs.directive',
    'plogsUtils'
]).factory('breadcrumbsModuleAssets', function (assets) {
    return function (path) {
        return assets("main/js/breadcrumbs/" + path);
    };
});
