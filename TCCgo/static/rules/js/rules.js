var app = angular.module("myApp", []);

app.controller("ruleController", function($scope, $http){
  $http.get('/rules/all_rules')
  .then(function(data){
    rules = JSON.parse(data.data);
    $scope.rules = rules;
  })
});
