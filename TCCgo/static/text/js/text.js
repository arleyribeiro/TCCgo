var app = angular.module("myApp", []);

app.controller("textController", function($scope, $http){
  $http.defaults.xsrfCookieName = 'csrftoken';
  $http.defaults.xsrfHeaderName = 'X-CSRFToken';

  $http.get('/text/all_texts')
  .then(function(data){
    var texts = data.data;
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

  $scope.editText = function(id){
    url = 'http://127.0.0.1:8000/text/edit_text/';
    window.sessionStorage.setItem('myID', id);
    //alert(window.sessionStorage.getItem('myID'));
    window.location = url;
  }

  $(document).ready(function(){
    /* Setting up behavior of elements */

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

      $http.post('/text/delete_text', $scope.text).then(function(data){
        /*  data.error :
            200 -> delete success
            300 -> delete error
            501 -> user error
        */
        if(data.status == 501){
          alert('Um usuário só pode deletar os próprios trabalhos.')
          return false;
        }else if(data.status == 200){
          alert('Trabalho deletado com sucesso!');
           location.reload();
        }else if(data.status == 300){
            alert('Trabalho não pode ser deletado no momento!');
        }
      });
    });

  });
});
