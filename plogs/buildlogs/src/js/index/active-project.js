var app = angular.module('index.project.factory', []);
app.factory('ActiveProjectFactory', function ProjectFactory($q, $http) {
    var exports = {};

    function getJson(url) {
        var deferred = $q.defer();
        $http.get(url)
            .then(function (response) {
                deferred.resolve(response.data);
            }, function (response) {
                deferred.reject(response.data);
            });
        return deferred.promise;
    }

    exports.getProject = function () {
        return getJson('/static/project-info.json');
    };

    exports.getStats = function () {
        return getJson('/static/project.json');
    };

    return exports;
});
