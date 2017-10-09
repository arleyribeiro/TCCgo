var app = angular.module("myApp", []);


app.controller("RuleController", function($scope, $http){
  /*
    Controller for the list of rules shown
  */
  // Setting up for post requests
  $http.defaults.xsrfCookieName = 'csrftoken';
  $http.defaults.xsrfHeaderName = 'X-CSRFToken';

  // Listing all rules of a user as loading page
  $http.get('/rules/all_rules')
  .then(function(response){
    $scope.rules = response.data['rules'];
  });

  // Filtering rules shown by search
  $scope.searchText = "";
  $scope.filterRules = function(){
    $http.post('/rules/filter_rules',
      {
        'search_text' : $scope.searchText
      }
    ).then(function(response){
      $scope.rules = response.data['filtered_rules'];
      $scope.$digest();
    });
  };

});

// Listing rule types (used in radio buttons)
app.controller("RuleTypeController", function($scope, $http){
  $http.get('/rules/all_types')
  .then(function(response){
    $scope.types = response.data['types'];
  })
});

function verify_name(name){
  /* Given a name, verify if it exists in database. If exists, return true */
  $.ajax({
    url: 'verify_name',
    method: 'get',
    data : {
      name : name
    },
    success: function(data){
      if(data.status){ // There is a rule with that name already
        $("#name-input").css("border", "2px solid red");
        $("#name-input").popover("show"/*{title: 'Nome já utilizado', content = 'Teste', trigger='hover'}*/);
      } else {
        $("#name-input").css("border", "none")
        $("#name-input").popover("hide");
      }
    },
    error: function(data){
      alert("Failure");
    }
  });
}

function validate_rule_form($form){
  /* Validate a form passed and return false if not valid, or a dict if valid */
  var fields = $form.serializeArray();
  var response = {}; // Will have all the fields
  $.each(fields, function(i, field){ // Loop form inputs
    if(field.value.length == 0){ // If any field is empty
      response = false;
      return response;
    } else{
      response[field.name] = field.value; // Add to the response to be sent to view
    }
  });
  return response;
}

function csrfSafeMethod(method) {
    // Used on setting the token to send Ajax
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function(){
  /* Setting up behavior of elements */

  // Adding token to AJAX
  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });

  $('#name-input').change(function(){
    /* Every time someone types a rule name, verify if it already exists in database*/
    verify_name($(this).val());
  });

  $('#new-rule-form').submit(function(event){
    /* Actions performed when send a new rule to be created */

    // Prevent submitting
    event.preventDefault();

    // Ask user if he is sure about it
    var confirmation = confirm("Tem certeza que deseja salvar a regra?");
    if(!confirmation){
      return false;
    }

    // Verify if there is empty fields and convert inputs into dict
    var response = validate_rule_form($(this));
    if(response === false){ // Some field is empty
      alert("Todos os campos devem ser preenchidos");
      return false;
    }
    else{ // All fields have something
      // Clearing form fields
      $('#new-rule-form').each(function(){
        this.reset()
      });

      // Hiding the form for later
      $('#new-rule-form').addClass("hide");
      // Returning the button
      $('#add-new-rule-button').removeClass("hide");

      // Start sending the new rule to be created
      $.ajax({
        url: $(this).attr('action'),
        method : $(this).attr('method'),
        data: response,
        dataType: 'json',
        success: function(response){

          // Adding the new rule to the page
          var rules_scope = angular.element($('#rules_container')).scope();
          rules_scope.$apply(function(){
            rules_scope.rules.push(response['new_rule']);
          });
          rules_scope.$digest();
        },
        error: function(response){
          alert("Failure");
        }
      });
    }
  });

  $(document).on('click', '#add-new-rule-button', function(){
    $new_form = $('#new-rule-form').clone() // Make a new hidden form for future creatings
    $('#new-rule-form').removeClass("hide");  // Make a form appear
    $(this).addClass("hide"); // Hide the button
    $(this).before($new_form);  // Insert the hidden form before the button
  });


  $(document).on('click', '.remove-button',  function(){
    // Way to remove rules in the rule list page
    var confirmation = confirm("Tem certeza que deseja deletar essa regra?");
    if(!confirmation){  // Respondeu nao
      return false;
    }
    var $parent_div = $(this).parent();
    var $grandparent_div = $parent_div.parent();
    var rule_name = $grandparent_div.siblings('.panel-heading').text();
    var response = {};
    response['rule_name'] = rule_name;
    $.ajax({
      url: 'delete_rule',
      method: 'post',
      data: response,
      success: function(data){
        alert('Regra deletada com sucesso!')

        // After deleting, update the page without deleted rule
        var rules_scope = angular.element($('#rules_container')).scope();
        rules_scope.$apply(function(){
          $.ajax({
            url: '/rules/all_rules',
            method: 'get',
            success: function(response){
                rules_scope.rules = response['rules'];
                rules_scope.$digest();
            }
          });
        });
      },
      error: function(){
        alert("Failure")
      }
    });
  });
});
