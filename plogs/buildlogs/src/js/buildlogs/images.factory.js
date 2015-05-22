var app = angular.module('buildlogs.images.factory', [
    'ngResource'
]);

app.factory('BuildLogImage', function BuildLogImage($resource, $http) {
    return $resource(
        '/api/people/:username/projects/:project/buildlogs/:log_id/images/:image_id.json',
        {
            username: "@project.user",
            project: "@project.slug",
            log_id: "@log_id",
            image_id: "@image_id"
        },
        {
            // api returns extra data as an object (count, etc)
            query: { method: 'GET', isArray: false },
            update:  { method: 'PUT' }
        }
    );
});