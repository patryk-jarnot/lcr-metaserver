angular.
  module('PlatoLoCoApp').
  config(['$routeProvider',
    function config($routeProvider) {
      $routeProvider.
        when('/query', {
          template: '<query-creator></query-creator>'
        }).
        when('/wait/:token', {
          template: '<wait-page></wait-page>'
        }).
        when('/about', {
          template: '<about-page></about-page>'
        }).
        when('/tutorial', {
          template: '<tutorial-page></tutorial-page>'
        }).
        when('/help', {
          template: '<help-page></help-page>'
        }).
        when('/api', {
          template: '<api-page></api-page>'
        }).
        when('/job', {
          template: '<job-finder></job-finder>'
        }).
        when('/proteins/:token', {
          template: '<protein-list></protein-list>'
        }).
        when('/protein/:token/:id', {
          template: '<protein-detail></protein-detail>'
        }).
        otherwise('/query');
    }
  ]);
