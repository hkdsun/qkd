angular
  .module('QKDiary')
  .factory('AuthenticationService', AuthenticationService)

  AuthenticationService.$inject = ['$http', '$cookieStore', '$rootScope', '$timeout', 'User'];
  function AuthenticationService($http, $cookieStore, $rootScope, $timeout, User) {
    var service = {};

    service.Login = Login;
    service.SetCredentials = SetCredentials;
    service.ClearCredentials = ClearCredentials;

    return service;
     
    function Login(username, password, callback) {
      User.authenticate({cmd: 'login'}, { username: username, password: password}).$promise.then(
        function(response) {
          response.success = true;
          callback(response);
        },
        function(err) {
          console.log("Couldn't authenticate", err)
        }
      );
    }

    function SetCredentials(username, password) {
      var authdata = Base64.encode(username + ':' + password);

      $rootScope.globals = {
        currentUser: {
        username: username,
        authdata: authdata
        }
      };

      $http.defaults.headers.common['Authorization'] = 'Basic ' + authdata; // jshint ignore:line
      $cookieStore.put('globals', $rootScope.globals);
    }

    function ClearCredentials() {
      $rootScope.globals = {};
      $cookieStore.remove('globals');
      $http.defaults.headers.common.Authorization = 'Basic';
    }
  }
