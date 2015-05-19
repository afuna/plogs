var app = angular.module('stringToNumber.directive', []);
app.directive('stringToNumber', function() {
  return {
    require: 'ngModel',
    link: function(scope, element, attrs, ngModel) {
      ngModel.$parsers.push(function(value) {
        return '' + value;
      });
      ngModel.$formatters.push(function(value) {
        var parsed = parseFloat(value, 10);
        return isNaN(parsed) ? undefined : parsed;
      });
    }
  };
});