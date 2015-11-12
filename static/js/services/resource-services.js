angular.module('QKDiary').factory('Entry', function($resource) {
  return $resource("/entries/:id", {}, {
    query: { method: "GET", isArray: false }
  });
});

angular.module('QKDiary').factory('User', function($resource) {
  return $resource("/users/:cmd", {}, {
    query: { method: "GET", isArray: false },
    authenticate: { method: "POST" }
  });
});
