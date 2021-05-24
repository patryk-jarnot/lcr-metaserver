'use strict';


angular.module('waitPage').component('waitPage', {
    templateUrl: 'wait-page/wait-page.template.html',
    controller: ['$routeParams', '$scope', '$window', 'Job',
        function ($routeParams, $scope, $window, Job) {
            $scope.url = window.location.origin + '/#!/wait/' + $routeParams.token;
            $scope.token = $routeParams.token;
            $scope.checkResult = function() {
                var response = Job.query({token: $routeParams.token});
                response.$promise.then(function (data) {
                    if (data.status.toLowerCase() == "finished") {
                        $window.location.href = '#!/proteins/' + $routeParams.token;
                    }
                    else if (data.status.toLowerCase() == "error") {
                        alert('Invalid query');
                        $window.location.href = '#!/query';
                    }
                    else {
                        setTimeout($scope.checkResult, 2000)
                    }
                });
            }
            setTimeout($scope.checkResult, 2000)
        }
    ]
  });

