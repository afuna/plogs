var app = angular.module('buildlogs', [
    'buildlogs.factory',
    'buildlogs.categories.factory',
    'buildlogs.partners.factory',
    'buildlogs.controller',
    'buildlogDetail.controller',
    'buildlogForm.controller',
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