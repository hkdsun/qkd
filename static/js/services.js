angular.module('QKDiary').factory('Entry', function($resource) {
    return $resource("/entries/:id", {}, {
        query: { method: "GET", isArray: false }
    });
});
