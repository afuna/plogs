var app = angular.module('buildlogs.factory', [
    'ngResource'
]);

app.factory('BuildLog', function BuildLog($resource, $http) {
    return $resource(
        '/api/people/:username/projects/:project_id/buildlogs/:log_id.json',
        {
            username: "@project.user",
            project_id: "@project.id",
            log_id: "@log_id",
        },
        {
            // api returns extra data as an object (count, etc)
            query: { method: 'GET', isArray: false },
            update:  { method: 'PUT' }
        }
    );
});