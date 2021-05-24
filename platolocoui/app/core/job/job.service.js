'use strict';

angular.
  module('core.job').
  factory('Job', ['$resource', 'base_url',
    function($resource, base_url) {
      return $resource(base_url + '/restapi/job/:token', {token:'@token'}, {
        query: {
          method: 'GET',
        }
      });
    }
  ]);
