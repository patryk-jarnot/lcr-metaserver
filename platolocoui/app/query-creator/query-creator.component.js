'use strict';

angular.
    module('queryCreator').
    component('queryCreator', {
        templateUrl: 'query-creator/query-creator.template.html',
        controller: ['$http', '$rootScope', '$scope', '$window', 'Query',
            function ($http, $rootScope, $scope, $window, Query) {
                var self = this;
                $scope.input_text = "";

                $scope.jobTitle = "";

                $scope.methods = {}
                $scope.methods.seg_default = true;
                $scope.methods.seg_intermediate = true;
                $scope.methods.seg_strict = true;
                $scope.methods.cast = true;
                $scope.methods.flps = true;
                $scope.methods.flps_strict = true;
                $scope.methods.simple = true;
                $scope.methods.gbsc = true;

                $scope.enrichment = {}
                $scope.enrichment.pfam = true;
                $scope.enrichment.phobius = true;
                $scope.enrichment.aafrequency = true;

                $scope.params = {}
                $scope.params.seg = {}
                $scope.params.seg.window = 12;
                $scope.params.seg.k1 = 2.2;
                $scope.params.seg.k2 = 2.5;
                $scope.params.cast = {}
                $scope.params.cast.threshold = 40;
                $scope.params.cast.matrix = 1;
                $scope.params.flps = {}
                $scope.params.flps.min_tract_len = 15;
                $scope.params.flps.max_tract_len = 500;
                $scope.params.flps.pval = 0.001;
                $scope.params.flps.regions = {}
                $scope.params.flps.regions.single = true;
                $scope.params.flps.regions.multiple = true;
                $scope.params.flps.regions.whole = false;
                $scope.params.simple = {}
                $scope.params.simple.score_mono = 1;
                $scope.params.simple.score_di = 1;
                $scope.params.simple.score_tri = 1;
                $scope.params.simple.score_tetra = 1;
                $scope.params.simple.score_penta = 1;
                $scope.params.simple.score_hexa = 1;
                $scope.params.simple.score_hepta = 1;
                $scope.params.simple.score_octa = 1;
                $scope.params.simple.score_nona = 1;
                $scope.params.simple.score_deca = 1;
                $scope.params.simple.window = 11;
                $scope.params.simple.num_of_rand = 100;
                $scope.params.simple.rand_method = 3;
                $scope.params.simple.stringency = 0.9;
                $scope.params.gbsc = {}
                $scope.params.gbsc.score = 3;
                $scope.params.gbsc.distance = 7;

                $scope.redirect = function(inputSequences, methods, enrichment, params) {
                    if (inputSequences.trim() == '') {
                        alert('You have to insert UniProt AC(s) or fasta sequence(s)');
                        return 0;
                    }
                    var response = Query.update({name: $scope.jobTitle, sequences: inputSequences, methods: methods, enrichment: enrichment, params: params});
                    response.$promise.then(function (data) {
                        if (typeof data.error !== 'undefined') {
                            alert(data.error)
                        }
                        else {
                            $rootScope.enrichment = enrichment;
                            $window.location.href = '#!/wait/' + data.token;
                        }
                    });
                }

                $scope.expandCollapseParams = function(method) {
                    var paramsDiv = document.getElementById(method + '_params');
                    var segExpander = document.getElementById('expand_' + method);
                    if (paramsDiv.style.display == 'block') {
                        paramsDiv.style.display = 'none';
                        segExpander.innerHTML = '&#9654;'
                    }
                    else {
                        paramsDiv.style.display = 'block';
                        segExpander.innerHTML = '&#9660;'
                    }
                }

                $scope.expandCollapseAllParams = function(isExpand) {
                    var methods = ['seg', 'cast', 'flps', 'simple', 'gbsc'];
                    for (var i=0; i<methods.length; i++) {
                        var method = methods[i];
                        var paramsDiv = document.getElementById(method + '_params');
                        var segExpander = document.getElementById('expand_' + method);

                        if (!isExpand) {
                            paramsDiv.style.display = 'none';
                            segExpander.innerHTML = '&#9654;'
                        }
                        else {
                            paramsDiv.style.display = 'block';
                            segExpander.innerHTML = '&#9660;'
                        }
                    }
                }

                $scope.submit = function() {
                    var inputSequences = '';
                    if ($scope.input_text.trim() == '') {
                        var file = document.getElementById("fileInput").files[0];
                        if (!file) {
                            alert('You have to insert UniProt AC(s), fasta sequence(s) or upload a file');
                            return 0;
                        }
                        var aReader = new FileReader();
                        aReader.readAsText(file, "UTF-8");
                        aReader.onload = function (evt) {
                            document.getElementById("fileInput").innerHTML = evt.target.result;
                            var fileSize = document.getElementById("fileInput").files[0].size;;
                            if (fileSize > 1048576) {
                                alert('File limit exceeded');
                                return 0;
                            }
                            if (aReader.result.includes(">")) {
                                inputSequences = aReader.result;
                                $scope.redirect(inputSequences,  $scope.methods,  $scope.enrichment, $scope.params);
                            }
                            else {
                                var lines = aReader.result.match(/\S+/g) || []
                                var query = 'https://www.uniprot.org/uniprot/?query='
                                if (lines.length > 2500) {
                                    alert("Number of sequences should not be greather than 2500")
                                    return 0;
                                }
                                for (var i=0; i<lines.length; i++) {
                                    var numOfNonWordChars = (lines[i].match(/\W/g) || []).length
                                    if (numOfNonWordChars > 0) {
                                        alert('Invalid uniprot AC: ' + lines[i]);
                                        return 0;
                                    }
                                    query += 'id%3A' + lines[i].trim()
                                    if (i !=lines.length-1) {
                                        query += "+OR+";
                                    }
                                }
                                query += '&format=fasta';
                                $http.get(query).then(function(response) {
                                    inputSequences = response.data;
                                    $scope.redirect(inputSequences,  $scope.methods,  $scope.enrichment, $scope.params);
                                });
                            }
                        }
                        aReader.onerror = function (evt) {
                            document.getElementById("fileInput").innerHTML = "error";
                        }
                    }
                    else {
                        if ($scope.input_text.includes(">")) {
                            var numOfSequences = ($scope.input_text.match(/^|\n>/g) || []).length
                            if (numOfSequences > 2500) {
                                alert("Number of sequences should not be greather than 2500")
                                return 0;
                            }
                            inputSequences = $scope.input_text;
                            $scope.redirect(inputSequences,  $scope.methods,  $scope.enrichment, $scope.params);
                        }
                        else {
                            var lines = $scope.input_text.match(/\S+/g) || []
                            var query = 'https://www.uniprot.org/uniprot/?query='
                            if (lines.length > 2500) {
                                alert("Number of sequences should not be greather than 2500")
                                return 0;
                            }
                            for (var i=0; i<lines.length; i++) {
                                var numOfNonWordChars = (lines[i].match(/\W/g) || []).length
                                if (numOfNonWordChars > 0) {
                                    alert('Invalid uniprot AC: ' + lines[i]);
                                    return 0;
                                }
                                query += 'id%3A' + lines[i].trim()
                                if (i !=lines.length-1) {
                                    query += "+OR+";
                                }
                            }
                            query += '&format=fasta';
                            $http.get(query).then(function(response) {
                                inputSequences = response.data;
                                $scope.redirect(inputSequences,  $scope.methods,  $scope.enrichment, $scope.params);
                            });
                        }
                    }
                }

                $scope.exampleUniprotIds = function() {
                    $scope.input_text = "Q6GZX3\n" +
                                        "P14922\n" +
                                        "Q1ZXH2"
                }

                $scope.exampleSequences = function() {
                    $scope.input_text = ">sp|Q6GZX3|002L_FRG3G Uncharacterized protein 002L OS=Frog virus 3 (isolate Goorha) GN=FV3-002L PE=4 SV=1\n" +
                                        "SIIGATRLQNDKSDTYSAGPCYAGGCSAFTPRGTCGKDWDLGEQTCASGFCTSQPLCAR\n" +
                                        "KKTQVCGLRYSSKGKDPLVSAEWDSRGAPYVRCTYDADLIDTQAQVDQFVSMFGESPSL\n" +
                                        "ERYCMRGVKNTAGELVSRVSSDADPAGGWCRKWYSAHRGPDQDAALGSFCIKNPGAADC\n" +
                                        "CINRASDPVYQKVKTLHAYPDQCWYVPCAADVGELKMGTQRDTPTNCPTQVCQIVFNML\n" +
                                        "DGSVTMDDVKNTINCDFSKYVPPPPPPKPTPPTPPTPPTPPTPPTPPTPPTPRPVHNRK\n" +
                                        "MFFVAGAVLVAILISTVRW\n" +
                                        ">sp|P14922|CYC8_YEAST General transcriptional corepressor CYC8 OS=Saccharomyces cerevisiae (strain ATCC 204508 / S288c) GN=CYC8 PE=1 SV=2\n" +
                                        "NPGGEQTIMEQPAQQQQQQQQQQQQQQQQAAVPQQPLDPLTQSTAETWLSIASLAETLG\n" +
                                        "GDRAAMAYDATLQFNPSSAKALTSLAHLYRSRDMFQRAAELYERALLVNPELSDVWATL\n" +
                                        "HCYLMLDDLQRAYNAYQQALYHLSNPNVPKLWHGIGILYDRYGSLDYAEEAFAKVLELD\n" +
                                        "HFEKANEIYFRLGIIYKHQGKWSQALECFRYILPQPPAPLQEWDIWFQLGSVLESMGEW\n" +
                                        "GAKEAYEHVLAQNQHHAKVLQQLGCLYGMSNVQFYDPQKALDYLLKSLEADPSDATTWY\n" +
                                        "LGRVHMIRTDYTAAYDAFQQAVNRDSRNPIFWCSIGVLYYQISQYRDALDAYTRAIRLN\n" +
                                        "YISEVWYDLGTLYETCNNQLSDALDAYKQAARLDVNNVHIRERLEALTKQLENPGNINK\n" +
                                        "NGAPTNASPAPPPVILQPTLQPNDQGNPLNTRISAQSANATASMVQQQHPAQQTPINSS\n" +
                                        "TMYSNGASPQLQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAHAQA\n" +
                                        "QAQAQAQAQAQAQAQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQLQPLPRQQLQQKG\n" +
                                        "SVQMLNPQQGQPYITQPTVIQAHQLQPFSTQAMEHPQSSQLPPQQQQLQSVQHPQQLQG\n" +
                                        "PQAQAPQPLIQHNVEQNVLPQKRYMEGAIHTLVDAAVSSSTHTENNTKSPRQPTHAIPT\n" +
                                        "APATGITNAEPQVKKQKLNSPNSNINKLVNTATSIEENAKSEVSNQSPAVVESNTNNTS\n" +
                                        "EEKPVKANSIPSVIGAQEPPQEASPAEEATKAASVSPSTKPLNTEPESSSVQPTVSSES\n" +
                                        "TTKANDQSTAETIELSTATVPAEASPVEDEVRQHSKEENGTTEASAPSTEEAEPAASRD\n" +
                                        "EKQQDETAATTITVIKPTLETMETVKEEAKMREEEQTSQEKSPQENTLPRENVVRQVEE\n" +
                                        "ENYDD\n" +
                                        ">sp|Q1ZXH2|FHKB_DICDI Probable serine/threonine-protein kinase fhkB OS=Dictyostelium discoideum GN=fhkB PE=3 SV=1\n" +
                                        "SQDIQTQNSYSDELYSSQIYSTQQPQQPQQQPQQQQSTFSSQQSQSSSYDFIYSTPQIH\n" +
                                        "QNSQNSQFSQNPLYDDFIHSTQNSYSQRVSSQRSYSQKSSSSQISFSQIPSSQIQSSQI\n" +
                                        "SSQIHSSQIPSSQNQSSQKSQFSFSQIPSSQIPSSQKRFFQSQNDDFVPSSQVTSLQDI\n" +
                                        "LPQPIQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQCQPQQQQTQQQQQQQQQQQQQQ\n" +
                                        "QQQQQQQQQQQTQQQQQQPQEDDDDYDDYDGYDNYEDFVYNEGEEGEEDYEDYEQENDD\n" +
                                        "DDEDEDDDDDDDDDDDDEEEEEESQQQHIRSRALQSRSSQSRPLLRSGFKSPISRLSQT\n" +
                                        "TSPEYIYISSQSNTHTNQLGQSSQQTNSPNVHFNSLQQKKKQQQQQQQQQQQQQQQQQQ\n" +
                                        "QQQQQQQQSQQIIGSQSSQSSQLPPTQPPVEVPVNLGRLIPINASHIPINLNLKREDRI\n" +
                                        "VGRSSSCDARLIDNYLTISGKHCEIYRADNLTCLKHIPLCKDKTDCHKNFGMLIVHDIS\n" +
                                        "NGSYINGELIGNGKTRILRSDDILSLGHPSGDLKFIFESEFQFNFILDIKDNVNNLNEN\n" +
                                        "DYKKLRTAYDNARIENKNCALRDYYFVKEIGSGGYGIVYEGLYKLNGKRVAIKHIDLLK\n" +
                                        "GSTSKSMELVSKEYNALKNIKHRNVIEFFDIVFSSTDCFFIVELATNDLSNLLRKRCVD\n" +
                                        "DDIKRICKQLLLGFNYLHNLGIVHRDLKPENILYNEFKQGFSIKITDFGLSSFVEESQY\n" +
                                        "QTFCGTPLFFAPEVIANNFFSNGYGKSCDLWSIGVTLYLSLCKYKPFIVDCRDLYHSFI\n" +
                                        "GNLGFTSKKWAKISNYAKDLVRRLLVIDPEHRITIKEALNHPWFTQDRRFFKKYPKHYK\n" +
                                        "RAQPKTQFFVECFNVYYDLKSETGFICFREHFDNLETNYALFKQNFDNNNNNNNNNNNN\n" +
                                        "NNNNNNNNNNNNINNNNNNINNNNINNNNNNNNNNNNNTNTNNINNNNNNYNNSHNHNN\n" +
                                        "NHNHNHNLNNHNHNNNHHHNHNHNHNHNHNHNHNHNHNHNHNHNHNNHNNNNNNNNNNN\n" +
                                        "NNNNNNNNNNNNNNNNNNNNNNNNNNNNYYNNNINNINNNINNNINNNNNYHQQYTQHT\n" +
                                        "M"
                }
            }
        ]
    });

