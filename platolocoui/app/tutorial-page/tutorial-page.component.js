'use strict';

var app = angular.module('tutorialPage')


app.component('tutorialPage', {
    templateUrl: 'tutorial-page/tutorial-page.template.html',
    controller: ['$routeParams', '$scope', '$http',
      function ($routeParams, $scope, $http) {
      }
    ]
  });
