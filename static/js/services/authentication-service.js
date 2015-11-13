angular
  .module('QKDiary')
  .factory('AuthenticationService', AuthenticationService)

  AuthenticationService.$inject = ['$http', '$cookieStore', '$rootScope', '$timeout', 'User'];
  function AuthenticationService($http, $cookieStore, $rootScope, $timeout, User) {
    var service = {};

    service.Login = Login;
    service.Logout = Logout;
    service.Register = Register;

    return service;
     
    function Login(username, password, callback) {
      User.authenticate({}, { username: username, password: password}).$promise.then(
        function(response) {
          response.success = true;
          callback(response);
        },
        function(err) {
          err.success = false;
          callback(err);
        }
      );
    }

    function Logout(callback) {
      User.logout({}, {}).$promise.then(
          function(response) {
            response.success = true;
            callback(response);
          },
          function(err) {
            err.success = false;
            callback(err);
          }
        );
    }

    function Register(user, callback) {
      User.register({}, user).$promise.then(
        function(response) {
          response.success = true;
          callback(response)
        },
        function(err) {
          err.success = false;
          callback(err)
        }
      );
    }
  }
