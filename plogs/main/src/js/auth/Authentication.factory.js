angular.module('auth.Authentication.factory', [])
    .factory('AuthenticationFactory', function($http) {
        var exports = {};
        exports.isAuthenticated = function isAuthenticated() {
            return $http.get('/api/auth')
                .then(function(response) {
                    return response.data;
                }, function(response) {
                    return response.data;
                })
        }
        return exports;
    });
