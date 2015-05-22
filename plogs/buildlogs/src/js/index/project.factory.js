var app = angular.module('index.project.factory', []);
app.factory('ProjectFactory', function ProjectFactory($q, $http) {
    var exports = {};

    var projects = {};
    function cacheProject(project) {
        projects[project.user + "/" + project.slug] = project;
    }
    function getCachedProject(username, project) {
        return projects[username + "/" + project];
    }

    // for the project, we can afford to use the cached copy
    exports.getProject = function(username, project_slug) {
        var deferred = $q.defer();

        var project = getCachedProject(username, project_slug);
        if (project) {
            deferred.resolve(project);
        } else {
            $http.get('/api/people/'+username+'/projects/'+project_slug+'.json')
                .then(function(response) {
                    cacheProject(response.data);
                    deferred.resolve(response.data);
                });
        }
        return deferred.promise;
    };

    // for the stats, we want to check whenever we can
    exports.getActiveProject = function () {
        return $http.get('/api/projects/active')
            .then(function (response) {
                cacheProject(response.data.project);
                return response.data;
            });
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
