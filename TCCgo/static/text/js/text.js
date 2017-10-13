var app = angular.module("myApp", []);

app.controller("textController", function($scope, $http){
  $http.defaults.xsrfCookieName = 'csrftoken';
  $http.defaults.xsrfHeaderName = 'X-CSRFToken';

  $http.get('/text/all_texts')
  .then(function(data){
    var texts = JSON.parse(data.data);
    $scope.texts = texts;
  })

  $scope.searchText = "";
  $scope.filterTexts = function(){
    $http.post('/text/filter_texts', {'search_text' : $scope.searchText})
    .then(function(response){
      var texts = JSON.parse(response.data);
      $scope.texts = texts;
      // $scope.$digest();
    });
  };


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

    $(document).on('click', '.remove-button',  function(e) {
      e.preventDefault();
      // Way to remove rules in the rule list page
      
      var confirmation = confirm("Tem certeza que deseja deletar esse trabalho? ");
      if(!confirmation){  // Respondeu nao
        return false;
      }
      var $parent_div = $(this).parent();
      var $grandparent_div = $parent_div.parent();
      var text_title = $grandparent_div.closest('.panel-heading.text').text().trimRight().trimLeft();
      var response =  text_title;
      $scope.text={
        text_title: ''
      }
      $scope.text.text_title=text_title;
      alert($scope.text.text_title+' ' +$scope.text.text_title.length);

      $http.post('/text/delete_text', $scope.text).then(function(data){
        if(data.status == 501){
          alert('Um usuário só pode deletar os próprios trabalhos.')
          return false;
        }
        alert('Trabalho deletado com sucesso!');
        location.reload();
      });
    });

  });
});
