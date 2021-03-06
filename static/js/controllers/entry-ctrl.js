/**
 * Entries Controller
 */

angular
    .module('QKDiary')
    .controller('EntriesCtrl', ['$scope', '$uibModal', '$resource', 'Entry', EntriesCtrl]);

function EntriesCtrl($scope, $uibModal, $resource, Entry) {
  $scope.formEntry = new Entry({body:""})

  var entries = Entry.query(function(data) {
    data.entries.map(function(en) {
      en.date = new Date(en.date)
    });
    $scope.entries = data.entries
  });

  $scope.updateEntry = function(entry, body) {
    Entry.get({id:entry.id}).$promise.then(function(r) {
      r.body = body
      r.$save({id:entry.id})
    }, function(errResponse) {
      console.log(errResponse)
    });
  };

  $scope.favoriteEntry = function(entry) {
    Entry.get({id:entry.id}).$promise.then(function(r) {
      if (r.favorite) {
        Entry.defavorite({id:r.id}, {}).$promise.then(function(r) {
          entry.favorite = false;
        }, function(err) {
          console.log(err)
        });
      } else {
        Entry.favorite({id:r.id}, {}).$promise.then(function(r) {
          entry.favorite = true;
        }, function(err) {
          console.log(err)
        });
      }
    }, function(errResponse) {
      console.log(errResponse);
    });
    
  };

  $scope.delete = function(entry) {
    Entry.remove({id:entry.id}).$promise.then(
    function(r) {
      var index = $scope.entries.indexOf(entry);
      if (index > -1) {
        $scope.entries.splice(index, 1);
      }
    }, 
    function(errResponse) {
    console.log(errResponse)
    });
  };

  $scope.newEntryModal = function () {
    var modalInstance = $uibModal.open({
      animation: true,
      templateUrl: 'static/templates/entry_modal.html',
      controller: 'EntryModalCtrl'
    });

    modalInstance.result.then(function (newEntry) {
      newEntry.$save(function(u, response){
        $scope.entries.push(u)
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
