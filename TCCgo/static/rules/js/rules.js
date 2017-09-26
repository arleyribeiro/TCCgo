var app = angular.module("myApp", []);

// Listing rules

app.controller("ruleController", function($scope, $http){
  $http.get('/rules/all_rules')
  .then(function(data){
    rules = JSON.parse(data.data);
    $scope.rules = rules;
  })
});

/* Adding new Rules */

// Add rule button config
$("#add-new-rule-button").click(function(){
  $template = $('#add-new-rule-template');
  // Create another template to add more rules
  $newform = $template.clone();
  // Show the pre-existent template
  $template.removeClass('hide');
  // Append the hided template
  $('#rules_container').append($newform);
  // Hide button while you add a new rule
  $(this).addClass('hide');
});

// POST form config
$("#add-new-rule-template").on('submit', function(){
  // Cancel the usual submit behavior
  event.preventDefault();
  // Return the button
  $('#add-new-rule-button').removeClass('hide');
  $.ajax({
    url: '/rules/create_rule',
    type: $(this).attr('method'),
    data: $(this).serialize(),
    success: function(response){
      alert("Success");
    },
    error: function(response){
      alert("Failure");
    }
  })
})
