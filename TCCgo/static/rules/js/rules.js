
$(document).ready(function(){
  counter = 0;
  $.ajax({
    url:'/rules/all_rules',
    dataType: 'json',
    success: function(data) {
      rules = JSON.parse(data);
       for(var i=0; i<rules.length; i++){
         $("#rules_container").append("<p>Rule: " + rules[i].fields.name + "</p>");
       }
    }
  })
});
