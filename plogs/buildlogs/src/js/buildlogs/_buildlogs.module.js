var app = angular.module('buildlogs', [
    'buildlogs.factory',
    'buildlogs.controller',
    'buildlogDetail.controller',
    'buildlogTitle.directive',
    'buildlogMetadata.directive',
    'buildlogText.directive',
    'buildlogImages.directive',
    'plogsUtils'
])
.factory('buildlogsModuleAssets', function (assets) {
    return function (path) {
        return assets("buildlogs/js/buildlogs/" + path);
    };
});