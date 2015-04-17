var app = angular.module('index.active-project.factory', []);
app.factory('ActiveProjectFactory', function ActiveProjectFactory($q, $http) {
    var exports = {};

    // for the project, we can afford to use the cached copy
    var project;
    exports.getProject = function() {
        var deferred = $q.defer();
        if (project) {
            deferred.resolve(project);
        } else {
            exports.getProjectStats()
                .then(function (response) {
                    project = response.project;
                    deferred.resolve(project);
                });
        }
        return deferred.promise;
    };

    // for the stats, we want to check whenever we can
    exports.getProjectStats = function () {
        var deferred = $q.defer();

        $http.get('/api/projects/active')
            .then(function (response) {
                deferred.resolve(response.data);
            }, function (response) {
                deferred.reject(response.data);
            });

        return deferred.promise;
    };

    /*
    Stubs out the project stats for less flicker
    (things moving around vertically on page load)
    */
    exports.stubProject = function () {
        return {
            project: {
            },
            stats: {
                hours: 0,
                sessions: 0,
                dollars: 0
            }
        };
    };

    return exports;
});
