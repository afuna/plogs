var app = angular.module('buildlogForm.controller', [
    'combobox.directive'
]);
app.controller('BuildLogFormController', function BuildLogFormController($scope, $routeParams, $location, $filter,
        Category, Partner, BuildLog, BuildLogImage) {
    this.form = {
        date: (new Date())
    };

    if ( $routeParams.log_id ) {
        BuildLog.get({
            username: $routeParams.username,
            project: $routeParams.project,
            log_id: $routeParams.log_id
        }).$promise
            .then(angular.bind(this, function then(data) {
                this.form = data;
                $scope.$broadcast('editor.init', data.notes_edit);
            }));
    }
    this.categories = [];
    Category.query({
        username: $routeParams.username
    }).$promise
        .then(angular.bind(this, function then(data) {
            this.categories = data.results;
        }));

    var addedCategoryAtIndex;
    this.processNewCategory = angular.bind(this, function(category) {
        if (addedCategoryAtIndex !== undefined ) {
            this.categories.splice(addedCategoryAtIndex, 1);
        }

        var newCategory = { name: category, id: 0 };
        addedCategoryAtIndex = this.categories.length;
        this.categories.push(newCategory);
        return newCategory;
    });

    this.partners = [];
    Partner.query({
        username: $routeParams.username
    }).$promise
        .then(angular.bind(this, function then(data) {
            this.partners = data.results;
        }));

    var addedPartnerAtIndex;
    this.processNewPartner = angular.bind(this, function(partner) {
        if (addedPartnerAtIndex !== undefined ) {
            this.partners.splice(addedPartnerAtIndex, 1);
        }

        var newPartner = { name: partner, id: 0 };
        addedPartnerAtIndex = this.partners.length;
        this.partners.push(newPartner);
        return newPartner;
    });

    this.save = function(buildlog) {
        buildlog.project = {"user": $routeParams.username, "slug": $routeParams.project};
        buildlog.date = $filter('date')(buildlog.date, "yyyy-MM-dd");

        var buildLogAPI = new BuildLog(buildlog);
        var promise;
        if (buildlog.log_id) {
            // edit
            promise = buildLogAPI.$update();
        } else {
            // create new
            promise = buildLogAPI.$save();
        }

        promise.then(function(response) {
            $location.url('/people/' + response.project.user +
                          '/projects/' + response.project.slug +
                          '/buildlogs/' + response.log_id);
        })
        .catch(function(response) {
            console.log("error saving buildlog", response);
        })
    };

    this.addImage = function(imageList) {
        return function(imageData) {
            imageList.push(imageData);
        }
    };

    this.deleteImage = function(event, image) {
        event.preventDefault();
        var index = this.form.images.indexOf(image);
        image.removed = true;

        if (index != -1) {
            BuildLogImage.remove({
                username: $routeParams.username,
                project: $routeParams.project,
                log_id: $routeParams.log_id,
                image_id: image.id
            }, angular.bind(this, function() {
                this.form.images.splice(index, 1);
            }));
        }
    };
});
