'use strict';


// Register `phoneList` component, along with its associated controller and template
angular.
  module('proteinList').
  component('proteinList', {
    templateUrl: 'protein-list/protein-list.template.html',
    controller: ['$routeParams', 'Proteins', '$scope', '$window', function ProteinListController($routeParams, Proteins, $scope, $window) {
        var self = this;
        this.orderProp = 'user_order';
        $scope.token = $routeParams.token;

        var response = Proteins.query({token: $routeParams.token})
        response.$promise.then(function (data) {
            $scope.name = data.name;
            if ($scope.name == null || $scope.name == '') {
                $scope.name_visible = false;
            }
            else {
                $scope.name_visible = true;
            }
            self.proteins = data.proteins;
            self.maxLength = 0;
            for (var i=0; i<self.proteins.length; i++) {
                if (self.proteins[i].length > self.maxLength) {
                    self.maxLength = self.proteins[i].length;
                }
            }
        })
        $scope.viewType = 'methodsStretched';
        $scope.viewChanged = function() {
            for (var i=0; i<self.proteins.length; i++) {
                var ctx = document.getElementById("canvas_"+self.proteins[i].id);
                var parent = ctx.parentNode;
                ctx.width = parent.offsetWidth - 20;
                if ($scope.viewType == 'methodsStretched')
                    proteinListAddMethods(ctx, self.proteins[i], -1)
                else if ($scope.viewType == 'methodsRelative')
                    proteinListAddMethods(ctx, self.proteins[i], self.maxLength)
                else if ($scope.viewType == 'consensusSum')
                    proteinListAddRanges(ctx, self.proteins[i]);
            }
        }

        $scope.token = $routeParams.token;
        $scope.bindCanvas = function(protein) {
            var ctx = document.getElementById("canvas_"+protein.id);
            var parent = ctx.parentNode;
            ctx.width = parent.offsetWidth - 20;
            if ($scope.viewType == 'methodsStretched')
                proteinListAddMethods(ctx, protein, -1)
            else if ($scope.viewType == 'methodsRelative')
                proteinListAddMethods(ctx, protein, self.maxLength)
            else if ($scope.viewType == 'consensusSum')
                proteinListAddRanges(ctx, protein);
        }

       angular.element($window).bind('resize', function() {
            for (var i=0; i<self.proteins.length; i++) {
                var ctx = document.getElementById("canvas_"+self.proteins[i].id);
                var parent = ctx.parentNode;
                ctx.width = parent.offsetWidth - 20;
                if ($scope.viewType == 'methodsStretched')
                    proteinListAddMethods(ctx, self.proteins[i], -1)
                else if ($scope.viewType == 'methodsRelative')
                    proteinListAddMethods(ctx, self.proteins[i], self.maxLength)
                else if ($scope.viewType == 'consensusSum')
                    proteinListAddRanges(ctx, self.proteins[i]);
            }
       });
    }]
  });
