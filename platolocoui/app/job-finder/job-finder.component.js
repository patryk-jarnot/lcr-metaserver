'use strict';


angular.module('jobFinder').component('jobFinder', {
    templateUrl: 'job-finder/job-finder.template.html',
    controller: ['$routeParams', '$scope', 'Job', '$window',
      function ($routeParams, $scope, Job, $window) {
            var self = this
            $scope.token = '';

            $scope.submitJobId = function() {
                var response = Job.query({token: $scope.token});
                response.$promise.then(function (data) {
                    if (data.status.toLowerCase() == "finished") {
                        $window.location.href = '#!/proteins/' + data.token;
                    }
                    else if (data.status.toLowerCase() == "processing") {
                        $window.location.href = '#!/wait/' + data.token;
                    }
                    else {
                        $scope.message = "Could not find your job ID";
                    }
                });
            }
            $scope.submitJobIdIfEnter = function(event) {
                if (event.keyCode == 13 || event.which == 13){
                    $scope.submitJobId();
                }
            }
      }
    ]
  });

