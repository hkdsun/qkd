angular
  .module('QKDiary')
  .controller('DropdownCtrl', ['$scope', '$resource', '$window', '$timeout', 'AuthenticationService', 'User', DropdownCtrl]);

function DropdownCtrl($scope, $resource, $window, $timeout, AuthenticationService, User) {
    $scope.logout = function() {
        AuthenticationService.Logout(function(response) {
            if (response.success) {
                $window.location.href = '/users/login';
            } else {
                console.log("couldn't log out");
            }
        });
    }
}
