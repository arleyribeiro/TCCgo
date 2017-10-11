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

  // listing all rule types inside radio buttons
  $http.get('/rules/all_types')
  .then(function(response){
    $scope.types = response.data['types'];
  })

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

  // Set edit mode for a rule
  $scope.edit = function(index){
    // Changing content of panel. TODO: specificate which div to edit in the list

    var prev_rule_name = $scope.rules[index].name; // Used to identify the rule being changed
    $('.rule').addClass('hide');
    $('.edit-rule').removeClass('hide');

    // Setting sending button behavior
    $(document).on('click', '#save-edit-button', function(){
      $http.post('/rules/update_rule',
        {
          'old_name' : prev_rule_name,
          'new_name' : $scope.rules[index].name,
          'new_pattern' : $scope.rules[index].pattern,
          'new_warning' : $scope.rules[index].warning,
          'new_scope' : $scope.rules[index].scope,
          // 'new_type' : $scope.rules[index].type // TODO: fix this (it's not sending anything)
        }
      ).then(function(response){
        $('.rule').removeClass('hide');
        $('.edit-rule').addClass('hide');
        if(response.data.status == 500){
          alert("O nome de regra já existe no sistema.")
          return false;
        }
        if(response.data.status == 501){
          alert('Um usuário só pode atualizar as próprias regras.')
          return false;
        }
        $scope.$digest();
      });
    })

    // Setting cancel button behavior
    $(document).on('click', '#cancel-edit-button', function(){
      $('.rule').removeClass('hide');
      $('.edit-rule').addClass('hide');
    });

    // TODO: get element by its index passed to the function (html element) to specificate the content to change
  }

});

app.controller("RuleTypeController", function($scope, $http){
  /* List rule types that the database have */
  $http.get('/rules/all_types')
  .then(function(response){
    $scope.types = response.data['types'];
  })
});

function verify_name(name, element){
  /* Given a name, verify if it exists in database. If exists, return true */
  $.ajax({
    url: 'verify_name',
    method: 'get',
    data : {
      name : name
    },
    success: function(data){
      if(data.status){ // There is a rule with that name already
        element.css("border", "2px solid red");
        element.popover("show"/*{title: 'Nome já utilizado', content = 'Teste', trigger='hover'}*/);
      } else {
        element.css("border", "none")
        element.popover("hide");
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
    verify_name($(this).val(), $(this));
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
    /* Show the new rule form */
    $new_form = $('#new-rule-form').clone() // Make a new hidden form for future creatings
    $('#new-rule-form').removeClass('hide');  // Make a form appear
    $('#new-rule-form').addClass('tmp-form'); // Used on cancel button
    $(this).addClass("hide"); // Hide the button
    $(this).before($new_form);  // Insert the hidden form before the button
  });

  $(document).on('click', '#cancel-button', function(){
    /* Cancel the creation of a new rule */
    $('#add-new-rule-button').removeClass('hide'); // Show the new rule button again
    $('.tmp-form').remove(); // Remove the temporary form created
  })


  $(document).on('click', '.remove-button',  function(){
    // Way to remove rules in the rule list page
    var confirmation = confirm("Tem certeza que deseja deletar essa regra?");
    if(!confirmation){  // Respondeu nao
      return false;
    }
    var $parent_div = $(this).parent();
    var $grandparent_div = $parent_div.parent();
    var rule_name = $grandparent_div.siblings('.panel-heading.rule').text();

    var response = {};
    response['rule_name'] = rule_name;
    $.ajax({
      url: 'delete_rule',
      method: 'post',
      data: response,
      success: function(data){
        if(data.status == 501){ // Not user rule
          alert('Um usuário só pode deletar as próprias regras.')
          return false;
        }
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
