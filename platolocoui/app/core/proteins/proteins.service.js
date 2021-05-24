'use strict';

angular.
  module('core.proteins').
  factory('Proteins', ['$resource', 'base_url',
    function($resource, base_url) {
      return $resource(base_url + '/restapi/proteins/:token', {token:'@token'}, {
        query: {
          method: 'GET',
        }
      });
    }
  ]);
