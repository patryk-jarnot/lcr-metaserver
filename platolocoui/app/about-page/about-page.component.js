'use strict';

var app = angular.module('aboutPage')


app.component('aboutPage', {
    templateUrl: 'about-page/about-page.template.html',
    controller: ['$routeParams', '$scope', '$http',
      function ($routeParams, $scope, $http) {
      }
    ]
  });
