var app = angular.module("myApp", []);

// Listing rules

app.controller("RuleController", function($scope, $http){
  $http.get('/rules/all_rules')
  .then(function(data){
    rules = JSON.parse(data.data);
    $scope.rules = rules;
  })
});

// Listing rule types
app.controller("RuleTypeController", function($scope, $http){
  $http.get('/rules/all_types')
  .then(function(data){
    types = JSON.parse(data.data)
    $scope.types = types;
  })
})

/* Adding new Rules */

function verify_name(name){
  // Given a name, verify if it exists in database. If exists, return true
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
  // Validate a form passed and return false if not valid, or a dict if valid
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

$('#name-input').change(function(){
  verify_name($(this).val());
});

$('#new-rule-form').submit(function(event){
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

  // Start sending the new rule to be created
  else{ // All fields have something
    $.ajax({
      url: $(this).attr('action'),
      method : $(this).attr('method'),
      data: response,
      dataType: 'json',
      success: function(response){
        alert("Regra Criada com sucesso");
        // As linhas abaixo não funcionam
        // var rules_scope = angular.element($('#rules_container')).scope();
        // rules_scope.$apply(function(){
        //   rules_scope.rules.push(response.rule);
        // });
        // rules_scope.$digest();
      },
      error: function(response){
        alert("Failure");
      }
    });
  }
});
