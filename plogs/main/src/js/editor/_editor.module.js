var app = angular.module('editor', [
    'editor.directive',
    'plogsUtils'
]).factory('editorModuleAssets', function (assets) {
    return function (path) {
        return assets("main/js/editor/" + path);
    };
});
