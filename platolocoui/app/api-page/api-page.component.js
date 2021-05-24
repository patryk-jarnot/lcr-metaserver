'use strict';

var app = angular.module('apiPage')


app.component('apiPage', {
    templateUrl: 'api-page/api-page.template.html',
    controller: ['$routeParams', '$scope', '$http',
      function ($routeParams, $scope, $http) {
      }
    ]
  });

