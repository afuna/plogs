var app = angular.module('breadcrumbs.directive', []);
app.directive('breadcrumbs', function (breadcrumbsModuleAssets) {
    return {
        restrict: 'E',
        templateUrl: breadcrumbsModuleAssets("partials/breadcrumbs.tmpl.html"),
        controllerAs: 'breadcrumbs',
        controller: function($location) {
            var path = $location.path().split("/");
            this.pages = [{url: "#/", "title": "Home"}];
            this.pages.push({url: "#" + path.slice(0, path.length - 1).join("/"), "title": "Buildlogs"});
            if (path[path.length - 2] === "buildlogs") {
                this.pages.push({url: "", "title": "#" + path[path.length-1]})
            }
        }
    };
});
