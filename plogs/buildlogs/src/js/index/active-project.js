var app = angular.module('index.active-project.factory', []);
app.factory('ActiveProjectFactory', function ActiveProjectFactory($q, $http) {
    var exports = {};

    exports.getProject = function () {
        var deferred = $q.defer();
        $http.get('/api/projects/active')
            .then(function (response) {
                deferred.resolve(response.data);
            }, function (response) {
                deferred.reject(response.data);
            });
        return deferred.promise;
    };

    return exports;
});
