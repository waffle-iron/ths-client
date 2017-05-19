(function() {
    /**
     * Created by diegofigs on 5/18/17.
     */
    'use strict';

    angular
        .module('thsClient.auth', [])
        .config([
            '$stateProvider',
            '$urlRouterProvider',
            Auth
        ]);

    function Auth($stateProvider, $urlRouterProvider) {

    }
})();
