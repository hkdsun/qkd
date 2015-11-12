angular
  .module('QKDiary')
  .controller('UserCtrl', ['$scope', '$resource', 'AuthenticationService', UserCtrl]);

function UserCtrl($scope, $resource, AuthenticationService) {
  $scope.vm = this;

  $scope.login = function() {
    vm = $scope.vm
    vm.dataLoading = true;
    AuthenticationService.Login(vm.username, vm.password, function(response) {
      if (response.success) {
        AuthenticationService.SetCredentials(vm.username, vm.password);
        $location.path('/');
      } else {
        FlashService.Error(response.message);
        vm.dataLoading = false;
      }
    });
  };

  $scope.register = function() {
      $scope.vm.dataLoading = true
      UserService.Create(vm.user)
      .then(function(response) {
          if (response.success) {
              FlashService.Success('Registration successful', true)
              $location.path('/login')
          } else {
              FlashService.Error(response.message)
              vm.dataLoading=false
          }
      })
  }
}
