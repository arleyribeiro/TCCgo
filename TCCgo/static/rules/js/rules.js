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
  $template.addClass('add-new-rule-form')
  // Append the hided template
  $('#rules_container').append($newform);
  // Hide button while you add a new rule
  $(this).addClass('hide');
});


// POST form config
$("#add-new-rule-template").submit(function(e){
  // Cancel the usual submit behavior
  e.preventDefault();

  // Return the button
  $('#add-new-rule-button').removeClass('hide');

  // Get the inputs value to send on Ajax
  var $inputs = $(".add-new-rule-form :input");
  var sending_data = {};
  $inputs.each(function(){
    sending_data[this.name] = $(this).val();
    $(this).siblings("label[for=" + $(this).attr('name') + "]").after("<span>" + $(this).val() + "</span>");
    $(this).remove();
  });
  $.ajax({
    url: $(this).attr('action'),
    type: $(this).attr('method'),
    data: sending_data,
    dataType: 'json',
    success: function(response){
      alert("Success");
    },
    error: function(response){
      alert("Failure");
    }
  })
})
