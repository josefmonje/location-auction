(function() {
'use strict;'

angular.module('app.routes', ['ngRoute',])
  .config(['$routeProvider',
    function($routeProvider) {
      $routeProvider
        .when('/:qs?', {
          templateUrl: '../partial/search.html'
        })
        .otherwise({
          redirectTo: '/'
        });
    }]);

})();
