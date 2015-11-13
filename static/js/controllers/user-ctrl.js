angular
  .module('QKDiary')
  .controller('UserCtrl', ['$scope', '$resource', '$window', '$timeout', 'AuthenticationService', 'User', UserCtrl]);

function UserCtrl($scope, $resource, $window, $timeout, AuthenticationService, User) {
  $scope.vm = this;

  $scope.login = function() {
    vm = $scope.vm
    vm.dataLoading = true;
    AuthenticationService.Login(vm.username, vm.password, function(response) {
      if (response.success) {
        $window.location.href = "/";
      } else {
        vm.error = "Invalid username or password";
        vm.dataLoading = false;
      }
    });
  };

  $scope.register = function() {
    vm = $scope.vm;
    vm.dataLoading = true
    console.log(vm)

    AuthenticationService.Register(vm.user ,function(response) {
        if (response.success) {
          vm.success = 'Registration successful. You will be redirected shortly'
          $timeout(function() {
            $window.location.href = "/users/login"
          }, 4000);
        } else {
          vm.error = 'Failed';
          vm.dataLoading=false
        }
    });
  }
}
