angular.module('QKDiary').factory('Entry', function($resource) {
  return $resource("/entries/:id", {}, {
    query: { method: "GET", isArray: false }
  });
});

angular.module('QKDiary').factory('User', function($resource) {
  return $resource("/users/:id", {}, {
    query: { method: "GET", isArray: false },
    authenticate: { url: '/users/login', method: "POST" },
    register: { url: '/users/register', method: "POST" },
    deauthenticate: { url: '/users/logout', method: "GET" }
  });
});
