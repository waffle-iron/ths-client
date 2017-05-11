/**
 * Created by diegofigs on 5/11/17.
 */
'use strict';

var app = angular.module('thsClient', [
    'ui.router'
]);

app.config(['$locationProvider', '$stateProvider', '$urlRouterProvider',
    function($locationProvider, $stateProvider, $urlRouterProvider) {
    // HTML5 Mode for compatibility with Flask
    $locationProvider.html5Mode(true);

    // State declarations
    $stateProvider
        .state('app', {
            abstract: true,
            url: '/',
            templateUrl: '/static/app.html',
            controller: 'AppCtrl'
        })
        .state({
            parent: 'app',
            name: 'home',
            url: '/home',
            templateUrl: '/static/partials/home.html',
            controller: 'AppCtrl'
        });

    $urlRouterProvider.otherwise('/home');
}]);

app.controller('AppCtrl', ['$scope', '$log', function($scope, $log) {
    $log.log('Hello World from the App Controller using the $log Service');
}]);