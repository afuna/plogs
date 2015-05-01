var app = angular.module('buildlogForm.controller', [
    'combobox.directive'
]);
app.controller('BuildLogFormController', function BuildLogFormController($routeParams, Category, Partner, BuildLog) {
    this.form = {
        date: (new Date())
    };

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
        var project = {"user": $routeParams.username, "id": $routeParams.project_id};
        var newBuildLog = new BuildLog({project: project});
        newBuildLog.$save();
    };
});
