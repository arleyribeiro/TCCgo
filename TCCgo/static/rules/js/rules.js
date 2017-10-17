var app = angular.module("myApp", []);


app.controller("RuleController", function($scope, $http){
  /*
    Controller for the list of rules shown
  */
  /* Setting up for post requests */
  $http.defaults.xsrfCookieName = 'csrftoken';
  $http.defaults.xsrfHeaderName = 'X-CSRFToken';

  /* GETTING DATA FROM DATABASE WHEN PAGE LOADS */
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

  /* SETTING UP SEARCH BAR BEHAVIOR*/

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

  /* SETTING UP EDIT MODE*/

  // All rules start out of edit-mode
  $.each($scope.rules, function(){
    this.edit_mode = false;
  });
  // When hitting edit button, it becomes in edit mode
  $scope.edit = function(index){
    // Changing content of panel.
    var prev_rule_name = $scope.rules[index].name; // Used to identify the rule being changed in the database
    $scope.rules[index].edit_mode = true;
    if($scope.rules[index] == undefined){
      alert("Preencha o tipo da regra");
      return false;
    }

    // Setting sending button behavior
    $(document).on('click', '#save-edit-button', function(){
      console.log("NOVO TIPO DE REGRA: " + $scope.rules[index].type);
      $http.post('/rules/update_rule',
        {
          'old_name' : prev_rule_name,
          'new_name' : $scope.rules[index].name,
          'new_pattern' : $scope.rules[index].pattern,
          'new_warning' : $scope.rules[index].warning,
          'new_scope' : $scope.rules[index].scope,
          'new_type' : $scope.rules[index].type
        }
      ).then(function(response){
        $scope.rules[index].edit_mode = false;
        if(response.data.status == 500){
          alert("O nome de regra já existe no sistema.")
          return false;
        }
        if(response.data.status == 501){
          alert('Um usuário só pode atualizar as próprias regras.')
          return false;
        }
        alert("Regra alterada com sucesso");
      }, function(err){
        console.log("ERROR: " + err.status);
      });
    })

    // Setting edit cancel button behavior
    $scope.cancel_edit = function(index){
      $scope.rules[index].edit_mode = false;
    }
  }

  /* SETTING UP ADD NEW RULE MODE */

  // Start out of new rule mode
  $scope.new_rule_mode = false;

  // Function that starts the new rule mode
  $scope.set_nr_mode = function(){
    // Change mode
    $scope.new_rule_mode = true;

    // Form submitting
    $(document).on('submit', '#new-rule-form', function(event){
      /* Actions performed when send a new rule to be created */
      // Prevent submitting
      event.preventDefault();
      // Ask user if he is sure about it
      // var confirmation = confirm("Tem certeza que deseja salvar a regra?");
      // if(!confirmation){
      //   return false;
      // }
      // Verify if there are empty fields and convert inputs into dict
      var data_to_send = validate_rule_form($(this));
      if(data_to_send === false || $scope.selectedType == undefined){ // Some field is empty
        alert("Todos os campos devem ser preenchidos");
        return false;
      }
      else{ // All fields have something
        // Change mode
        data_to_send['rule_type'] = $scope.selectedType.type;
        $scope.new_rule_mode = false;
        // Prepare form to be user again
        $('#new-rule-form')[0].reset()
        // Start sending the new rule to be created
        $http.post($(this).attr('action'), data_to_send)
          .then(function(response){
            // Adding the new rule to the page
            $scope.rules.push(response.data['new_rule']);
            alert("Regra criada com sucesso.")
          }, function(err){
            console.log("ERROR: " + err.status);
          });
      }
    });
  }

  // Cancel new rule mode
  $scope.unset_nr_mode = function(){
    $scope.new_rule_mode = false;
  }

  // Get value from types select box
  $scope.setRuleType = function(index, item){
    $scope.rules[index].type = item.type;
  }

  /* SETTING UP RULE DELETE */

  $scope.delete = function(index){

    // Ask for confirmation
    var confirmation = confirm("Tem certeza que deseja deletar essa regra?");
    if(!confirmation){  // Respondeu nao
      return false;
    }
    // Get the rule name to delete
    var delete_name = $scope.rules[index].name;
    // Send request
    $http.post('delete_rule', {'rule_name' : delete_name})
      .then(function(response){
          if(response.data.status == 501){
            alert("Um usuário só pode deletar as próprias regras.")
            return false;
          }
          // Remove from rules
          $scope.rules.splice(index, 1);
          alert("Regra deletada com sucesso.")
      }, function(err){
        console.log("ERROR: " + err.status);
      }
    );
  }
});

$(document).ready(function(){
  /* Behaviors that I couldn't adapt to angular */

  $('#name-input').change(function(){
    /* Every time someone types a rule name, verify if it already exists in database*/
    verify_name($(this).val(), $(this));
  });
});

/* AUXILIARY FUNCTIONS*/

function verify_name(name, element){
  /* Given a name, verify if it exists in database. If exists, return true
     Obs: This function can't retrieve rule type beacuse it's in a select box of angular. This case is treated after
  */

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
