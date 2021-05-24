'use strict';

angular.
  module('core.query').
  factory('Query', ['$resource', 'base_url',
    function($resource, base_url) {
      return $resource(base_url + '/restapi/query', {}, {
        update: {
          method: 'PUT'
        }
      });
    }
  ]);
