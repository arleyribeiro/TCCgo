var app = angular.module("myApp", []);
app.controller("loginController", function($scope, $http){
  $http.defaults.xsrfCookieName = 'csrftoken';
  $http.defaults.xsrfHeaderName = 'X-CSRFToken';

  $scope.user={
    email: '',
    password: ''
  };
  $scope.invalid = false;

  myForm.email.onclick = function(){
    $scope.invalid = false;
  }

  myForm.password.onclick = function(){
    $scope.invalid = false;
  }

  $scope.send = function (e) {
      e.preventDefault();
      $http.post('/auth/check_login', $scope.user).then(function(response){
        if(response.data['success']){
            var url_atual = window.location.href;
            var sep1 = url_atual.split("=").pop();

            if(sep1==url_atual){
              window.location = response.data['url']
            }else{
              window.location = response.data['url']+sep1;
            }
        }
        else{
          $scope.invalid = true;
        }
      });
    }


});
