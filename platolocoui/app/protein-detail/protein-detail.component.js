'use strict';


angular.module('proteinDetail').component('proteinDetail', {
    templateUrl: 'protein-detail/protein-detail.template.html',
    controller: ['$http', '$routeParams', '$rootScope', '$scope', 'Protein',
      function ($http, $routeParams, $rootScope, $scope, Protein) {
        this.uniprot_id = $routeParams.uniprot_id;
            var self = this

            $('#popover_pfam').popover({ html: true, placement: 'right', trigger: 'click', content: '', template: '<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>', title: function() { return $(".pop-title").html(); }, })
            $('#popover_aa_freq').popover({ html: true, placement: 'right', trigger: 'click', content: '', template: '<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>', title: function() { return $(".pop-title").html(); }, })
            $('#popover_region_details').popover({ html: true, placement: 'right', trigger: 'click', content: '', template: '<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>', title: function() { return $(".pop-title").html(); }, })
            $('#popover_sequence_details').popover({ html: true, placement: 'right', trigger: 'click', content: '', template: '<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>', title: function() { return $(".pop-title").html(); }, })
            $('#popover_method_consensus').popover({ html: true, placement: 'right', trigger: 'click', content: '', template: '<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>', title: function() { return $(".pop-title").html(); }, })

            self.protein = Protein.query({token: $routeParams.token, id: $routeParams.id}, function(protein) {

                $scope.aafrequency_visible = protein.aafrequency;
                if (typeof protein.data.enrichment !== 'undefined' && protein.aafrequency) {
                    var chartData = enrichmentToChartData(protein.data.enrichment);
                    $scope.labels = chartData[0];
                    $scope.data = chartData[1];
                }
                $scope.header = protein.header;
                $scope.uniprot_id = protein.uniprot_id;
                $scope.sequence = protein.sequence;
                $scope.methods = processMethods(protein);
                for (var i=0; i<$scope.methods.length; i++) {
                    $scope.methods[i].isSelected = true;
                }
                var ft = 0;
                if (typeof protein.data.enrichment !== 'undefined' && typeof protein.data.entropy !== 'undefined' && typeof protein.data.wrapper !== 'undefined') {
                    ft = $scope.initializeFeatureViewer(protein.sequence, protein.data.wrapper, protein.data.entropy, protein.data.enrichment, self.protein, $scope);
                }
                $scope.consensusType = "intersection"

                if (protein.pfam) {
                    $http.get('https://pfam.xfam.org/protein/' + protein.uniprot_id + '?output=xml').then(function(response) {
                        var result1 = xml2js(response.data, {compact: true, spaces: 4});
                        pfamAddIntervals(ft, result1);
                        pfamFillDetails($http, $scope, result1);
                    });
                }
                var consensusResult = createConsensusSequence($scope.sequence, $scope.methods, $scope.consensusType);
                $scope.consensusSequence = consensusResult.sequence;
                $scope.consensusRegions = consensusResult.regions;
            });
            $scope.protein = self.protein;

          $scope.series = ['Sequence', 'SwissProt', 'nextProt', 'DisProt', 'PDB'];
          $scope.colors = ['rgb(234,189,93)', 'rgb(203,91,90)', 'rgb(40,153,40)', 'rgb(25,25,143)', 'rgb(64,50,79)'];
          $scope.options = {'legend': {'display': true}, 'scales': {'yAxes': [{'scaleLabel': {'display' : true, 'labelString': 'Frequency'}}], 'xAxes': [{'scaleLabel': {'display' : true, 'labelString': 'Amino acids'}}]}}
          Chart.plugins.register({
          beforeDraw: function(chartInstance) {
            $scope.chartInstance = chartInstance;
            var ctx = chartInstance.chart.ctx;

            if ($scope.fv.mode == "zoom") {
                ctx.fillStyle = "white";
                ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
                ctx.fillStyle = "rgba(0,0,0,0.05)";
            }
            else if ($scope.fv.mode == "select") {
                ctx.fillStyle = "white";
                ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
                ctx.fillStyle = "rgba(255,0,0,0.05)";
            }
            else {
                ctx.fillStyle = "white";
            }
            ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
            ctx.fillStyle = "#555";
            ctx.font = "15px Arial";
            ctx.textAlign = 'end';
            ctx.fillText($scope.fv.begin + " - " + $scope.fv.end, 990, 8);
          }
        });
            $scope.consensusChanged = function () {
                var consensusResult = createConsensusSequence($scope.sequence, $scope.methods, $scope.consensusType);
                $scope.consensusSequence = consensusResult.sequence;
                $scope.consensusRegions =  consensusResult.regions;
            }
            $scope.expandPdb = function (divId) {
                var pdbDiv = document.getElementById(divId);
                pdbDiv.style.display = 'block';
            }
            $scope.collapsePdb = function (divId) {
                var pdbDiv = document.getElementById(divId);
                pdbDiv.style.display = 'none';
            }


            $scope.is_alert_printed = false;
            $scope.bindCanvas = function(method, region) {

                var canvas_id = "canvas_" + method.method + "_" + region.i
                var ctx = document.getElementById(canvas_id);

                if (ctx == null && !$scope.is_alert_printed) {
                    $scope.is_alert_printed = true;
                }
                else if (ctx != null) {
                    ctx.width = 200;
                    ctx.height = 20;

                    regionMarker(ctx, ctx.width, 20, region.beg, region.end, $scope.sequence.length);
                }
            }

            $scope.bindCanvasPfam = function(pfamRegion) {

//                var canvas_id = "canvas_" + method.method + "_" + region.i
                var canvas_id = "pfam_" + pfamRegion.pfamacc + "_" + pfamRegion.beg + "_" + pfamRegion.end;
                var ctx = document.getElementById(canvas_id);

                if (ctx == null && !$scope.is_alert_printed) {
                    $scope.is_alert_printed = true;
                }
                else if (ctx != null) {
                    ctx.width = 200;
                    ctx.height = 20;

                    regionMarker(ctx, ctx.width, 20, pfamRegion.beg, pfamRegion.end, $scope.sequence.length);
                }
            }

            $scope.downloadFv = function(element) {
                var canvas = document.createElement('canvas');
                var context = canvas.getContext('2d');
                var fv = document.getElementById(element);
                var svg = fv.getElementsByTagName('svg')[0];
                var v = canvg.Canvg.fromString(context, svg.outerHTML);
                v.render();
                var img = canvas.toDataURL("image/png");

                var rawImageData = img.replace("image/png", "image/octet-stream");
                var element = document.createElement('a');
                element.setAttribute('href', rawImageData);
                element.setAttribute('download', "featureviewer.png");
                element.style.display = 'none';
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);

            }

            $scope.downloadAaFreq = function (elementId) {
                var canvas = document.getElementById(elementId);
                var ctx = canvas.getContext("2d");
                var img = canvas.toDataURL("image/png");
                var rawImageData = img.replace("image/png", "image/octet-stream");

                var element = document.createElement('a');
                element.setAttribute('href', rawImageData);
                element.setAttribute('download', "aafrequency.png");
                element.style.display = 'none';
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);
            }

            $scope.downloadAaFreqCsv = function () {
                var table = aafreqCreateCsv(self.protein.data.enrichment, $scope.sequence, $scope.fv.begin, $scope.fv.end);
                var data = new Blob([table], {type: 'text/plain'});
                var url = window.URL.createObjectURL(data);

                var element = document.createElement('a');
                element.setAttribute('href', url);
                element.setAttribute('download', "aafrequency.csv");
                element.style.display = 'none';
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);
            }

            $scope.downloadFastaLcrs = function () {
                var fasta = "";

                for (var i=0; i<$scope.consensusRegions.length; i++) {
                    var beg = $scope.consensusRegions[i].beg;
                    var end = $scope.consensusRegions[i].end;
                    fasta += $scope.header + "|" + beg + "|" + end + "\n";
                    fasta += $scope.sequence.substring(beg, end) + "\n";
                }


                var data = new Blob([fasta], {type: 'text/plain'});
                var url = window.URL.createObjectURL(data);

                var element = document.createElement('a');
                element.setAttribute('href', url);
                element.setAttribute('download', "lcrs.fasta");
                element.style.display = 'none';
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);
            }

            $scope.initializeFeatureViewer = function (sequence, wrapper, entropy, enrichment) {
                var localScope = $scope
                var phobius = enrichment.phobius
                var ft = new FeatureViewer(sequence,
                                           '#fv1',
                                            {
                                                showAxis: true,
                                                showSequence: true,
                                                brushActive: true, //zoom
                                                toolbar:true, //current zoom & mouse position
                                                bubbleHelp:true,
                                                zoomMax:50 //define the maximum range of the zoom
                                            });

                wrapperAddIntervals(ft, wrapper, sequence);
                entropyAddChart(ft, entropy);
                phobiusAddIntervals(ft, phobius);
                $scope.fv = {}
                $scope.fv.begin = 1
                $scope.fv.end = localScope.sequence.length;
                ft.onZoom(function(data, data2) {
                    $scope.fv.begin = data.detail.start;
                    $scope.fv.end = data.detail.end;
                    if ($scope.fv.begin == 1 && $scope.fv.end == $scope.sequence.length) {
                        $scope.fv.mode = "whole";
                    }
                    else {
                        $scope.fv.mode = "zoom";
                    }
                    localScope.data[0] = recalculateSequenceFreq(localScope.sequence.substring(data.detail.start, data.detail.end), self.protein.data.enrichment);
                    localScope.$apply();
                });
                ft.onFeatureSelected(function(data) {
                    $scope.fv.begin = data.detail.start;
                    $scope.fv.end = data.detail.end;
                    $scope.fv.mode = "select";
                    localScope.data[0] = recalculateSequenceFreq(localScope.sequence.substring(data.detail.start, data.detail.end), self.protein.data.enrichment);
                    localScope.$apply();
                });
                //ft.onFeatureDeselected(function(data) {
                //    $scope.fv.begin = 1
                //    $scope.fv.end = localScope.sequence.length;
                //    $scope.fv.mode = "whole";
                //    localScope.data[0] = recalculateSequenceFreq(localScope.sequence, self.protein.data.enrichment);
                //    localScope.$apply();
                //});
                return ft
            }
      }
    ]
  });


app.filter('trustAsHtml',['$sce', function($sce) {
    return function(text) {
      return $sce.trustAsHtml(text);
    };
  }]);
