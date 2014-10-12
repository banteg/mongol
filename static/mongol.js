var app = angular.module('mongol', []);

app.controller('LogsCtrl', function ($scope, $http) {
    console.log('mongol here');
    $scope.logs = [];

    $http.get('/api/last/10').success(function (data) {
        $scope.logs = data.data;
        console.log($scope.logs);
    })

    var source = new EventSource('/api/stream');
    source.onmessage = function (event) {
        $scope.logs.unshift(angular.fromJson(event.data));
        $scope.$apply();
        console.log($scope.logs.length);
    }
})
