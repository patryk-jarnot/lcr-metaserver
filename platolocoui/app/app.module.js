'use strict';

// Define the `phonecatApp` module
angular.module('PlatoLoCoApp', [
    // ...which depends on the `phoneList` module
    'ngRoute',
    'chart.js',
    'waitPage',
    'apiPage',
    'helpPage',
    'tutorialPage',
    'aboutPage',
    'jobFinder',
    'queryCreator',
    'proteinList',
    'proteinDetail'
]).constant('base_url', "http://127.0.0.1:5002");
