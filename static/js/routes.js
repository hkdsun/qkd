'use strict';

/**
 * Route configuration for the QKDiary module.
 */
angular.module('QKDiary').config(['$stateProvider', '$urlRouterProvider',
    function($stateProvider, $urlRouterProvider) {

        // For unmatched routes
        $urlRouterProvider.otherwise('/');

        // Application routes
        $stateProvider
            .state('index', {
                url: '/',
                templateUrl: 'static/templates/dashboard.html'
            })
    }
]);
