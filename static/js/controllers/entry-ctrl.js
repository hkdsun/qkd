/**
 * Entries Controller
 */

angular
    .module('QKDiary')
    .controller('EntriesCtrl', ['$scope', '$http', '$resource', 'Entry', EntriesCtrl]);

function EntriesCtrl($scope, $http, $resource, Entry) {
  var entries = Entry.query(function(data) {
    $scope.entries = data.entries
  });
}
