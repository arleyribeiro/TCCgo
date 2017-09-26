var app = angular.module("myApp", []);

// Listing rules

app.controller("ruleController", function($scope, $http){
  $http.get('/rules/all_rules')
  .then(function(data){
    rules = JSON.parse(data.data);
    $scope.rules = rules;
  })
});

// Adding new Rules

$("#add-new-rule-button").click(function(){
  var $input_rule = '<div class="panel panel-primary" id="new_rule">' +
                    ' <div class="panel-heading">' +
                    '   <label for="rule_title">Nome: </label>' +
                    '   <input type="text" name="rule_title">' +
                    ' </div>' +
                    ' <div class="panel-body">' +
                    '   <div class="col-md-6">' +
                    '     <label for="pattern">Padrão: </label>' +
                    '     <input type="text" name="pattern"><br>' +
                    '     <label for="warning">Aviso: </label>' +
                    '     <input type="text" name="warning"><br>' +
                    '  </div>' +
                    '  <div class="col-md-1 col-md-offset-2">' +
                    '   <button type="submit" class="btn btn-success">Salvar</button>' +
                    '  </div>' +
                    '  <div class="col-md-1 col-md-offset-1">' +
                    '   <button type="button" class="btn btn-danger">Cancelar</button>' +
                    '  </div>' +
                    ' </div>' +
                    '</div>';
  $("#rules_container").append($input_rule);
});
