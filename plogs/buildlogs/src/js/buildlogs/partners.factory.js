var app = angular.module('buildlogs.partners.factory', [
    'ngResource'
]);

app.factory('Partner', function Partner($resource, $http) {
    return $resource(
        '/api/people/:username/partners',
        {
            username: "@partner.user.username"
        },
        {
            // api returns extra data as an object (count, etc)
            query: { method: 'GET', isArray: false }
        }
    );
});