
$(document).ready(function(){
  counter = 0;
  $.ajax({
    url:'/rules/all_rules',
    dataType: 'json',
    success: function(data) {
      new_data = JSON.parse(data);
      alert(data);
      // for (rules in data){
      //   conter++;
      // }
      // alert(counter);
    }
  })
});
