var app = angular.module('buildlogs.categories.factory', [
    'ngResource'
]);

app.factory('Category', function Category($resource, $http) {
    return $resource(
        '/api/people/:username/categories',
        {
            username: "@category.user.username"
        },
        {
            // api returns extra data as an object (count, etc)
            query: { method: 'GET', isArray: false }
        }
    );
});