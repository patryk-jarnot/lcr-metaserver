'use strict';

angular.
  module('core.protein').
  factory('Protein', ['$resource', 'base_url',
    function($resource, base_url) {
      return $resource(base_url + '/restapi/proteins/:token/:id', {token: '@token', id: '@id'}, {
        query: {
          method: 'GET',
        }
      });
    }
  ]);
