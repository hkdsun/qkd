/**
 * Entries Controller
 */

angular
    .module('QKDiary')
    .controller('EntriesCtrl', ['$scope', '$uibModal', '$resource', 'Entry', EntriesCtrl]);

function EntriesCtrl($scope, $uibModal, $resource, Entry) {
  $scope.formEntry = new Entry({body:""})

  var entries = Entry.query(function(data) {
    $scope.entries = data.entries
  });

  $scope.open = function () {
    var modalInstance = $uibModal.open({
      animation: true,
      templateUrl: 'static/templates/entry_modal.html',
      controller: 'EntryModalCtrl',
      resolve: {
        items: function () {
          return $scope.items;
        }
      }
    });

    modalInstance.result.then(function (newEntry) {
      newEntry.$save(function(u, response){
        $scope.entries.push(u.entry)
      });
    });
  };
}

angular
    .module('QKDiary')
    .controller('EntryModalCtrl', ['$scope', '$uibModalInstance', 'Entry', EntryModalCtrl])

function EntryModalCtrl($scope, $uibModalInstance, Entry) {
  $scope.ok = function () {
    newEntry = new Entry({body:$scope.formEntry.body, date:new Date()});
    $uibModalInstance.close(newEntry);
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
}
