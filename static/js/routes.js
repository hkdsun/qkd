'use strict';

/**
 * Route configuration for the QKDiary module.
 */
angular.module('QKDiary').config(['$locationProvider', '$stateProvider', '$urlRouterProvider',
    function($locationProvider, $stateProvider, $urlRouterProvider) {
        $locationProvider.html5Mode(true);

        // For unmatched routes
        $urlRouterProvider.otherwise('/');

        // Application routes
        $stateProvider
            .state('index', {
                url: '/',
                templateUrl: 'static/templates/dashboard.html'
            })
            .state('register', {
                url: '/users/register',
                templateUrl: 'static/templates/sign-up.html'
            })
            .state('login', {
                url: '/users/login',
                templateUrl: 'static/templates/sign-in.html'
            })
    }
]);
