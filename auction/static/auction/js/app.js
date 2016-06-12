(function() {
'use strict;'
angular.module('app', ['app.ctrl', 'app.routes'])
  .config(['$httpProvider',
    function($httpProvider) {
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }])
  .config(['$interpolateProvider',
    function($interpolateProvider) {
      $interpolateProvider.startSymbol('[[').endSymbol(']]')
    }])
  .config(['uiGmapGoogleMapApiProvider',
    function(uiGmapGoogleMapApiProvider) {
      uiGmapGoogleMapApiProvider.configure({
        // key: 'your api key',
        v: '3.17',
      });
    }])

angular.module('app.ctrl', ['uiGmapgoogle-maps'])
  .filter('greaterthan', function () {
    return function (items, value) {
      var filteredItems = []
      angular.forEach(items, function (item){
        if (item.properties.price > value) {
          filteredItems.push(item);
        };
      });
      return filteredItems;
    }
  })
  .filter('lessthan', function () {
    return function (items, value) {
      var filteredItems = []
      angular.forEach(items, function (item){
        if (item.properties.price < value) {
          filteredItems.push(item);
        };
      });
      return filteredItems;
    }
  })
  .directive('googleplace', function($location) {
    return {
      require : 'ngModel',
      link : function(scope, element, attrs, model) {
        var swBound = new google.maps.LatLng(49.00, -8.00);
        var neBound = new google.maps.LatLng(61.00, -1.00);
        var uk = new google.maps.LatLngBounds(swBound, neBound);
        var options = { bounds : uk };

        scope.gPlace = new google.maps.places.Autocomplete(element[0], options);
        google.maps.event.addListener(scope.gPlace, 'place_changed',
          function() {
            scope.$apply(function() {
              model.$setViewValue(element.val());
            });
            var place = scope.gPlace.getPlace();
            var latitude = place.geometry.location.k;
            var longitude = place.geometry.location.D;
            var radius = scope.radius || 3;
            var qs = '?';

            if (latitude && longitude) {
              qs = qs + 'latitude=' + latitude +'&';
              qs = qs + 'longitude=' + longitude;
            }
            if (radius) {
              qs = qs + '&radius=' + radius;
            };

            // fires on autocomplete search
            scope.getData(qs);
            scope.input = '';
          });
      }
    };
  })
  .controller('mapCtrl', ['$filter', '$http', '$location', '$routeParams', '$scope', '$timeout', 'uiGmapGoogleMapApi',
    function mapCtrl($filter, $http, $location, $routeParams, $scope, $timeout, uiGmapGoogleMapApi) {
      $scope.listview = false;

      $scope.switch = function() {
        $scope.listview =! $scope.listview
      }

      // Events
      var showing = {};
      $scope.mapEvents = {
        click: function (gMap, eventName, model) {
          if ($scope.data[$scope.data.indexOf(showing)]) {
            $scope.data[$scope.data.indexOf(showing)].show = false
            $scope.list = $scope.data
            $scope.$apply();
          }
        }
      };

      $scope.markersEvents = {
        click: function (gMarker, eventName, model) {
          if ($scope.data[$scope.data.indexOf(showing)]) {
            $scope.data[$scope.data.indexOf(showing)].show = false
            $scope.$apply();
          }
          showing = model;
          model.show = (!model.show);
          $scope.$apply();
        }
      };

      $scope.detailEvents = {
        mouseover: function (gMarker, eventName, model) {
          model.show = true;
          $scope.$apply();
        },
        mouseout: function (gMarker, eventName, model) {
          $timeout(function() {
            model.show = false;
            $scope.$apply();
          }, 2000);
        }
      };

      // Filter functionality
      $scope.filterList = function() {
        var data = $scope.data;
        var by_auctioneer = $filter('filter')(data, $scope.auctioneer);
        var by_minprice = $filter('greaterthan')(data, $scope.minprice);
        var by_maxprice = $filter('lessthan')(data, $scope.maxprice);
        var collection = []

        if ($scope.auctioneer) {
          collection.push(by_auctioneer);
        };
        if ($scope.minprice) {
          collection.push(by_minprice);
        };
        if ($scope.maxprice) {
          collection.push(by_maxprice);
        };

        if (collection.length == 1) {
          $scope.list = collection[0];
        } else {
          var common = collection[0].filter(function(c){
            return collection[1].indexOf(c) != -1;
          });
          $scope.list = common;
        }
        if (collection.length == 3) {
          $scope.list = common.filter(function(c){
            return collection[2].indexOf(c) != -1;
          });
        }
      };

      // Fetches data from api
      $scope.getData = function(input) {
        var auction_api = '../mapapi/auction-data/';
        var sold_api = '../../mapapi/sold-data/';

        if ($scope.mode == 'detail') {
          api = sold_api;
        } else {
          api = auction_api;
        }

        if (input) {
          api = api + input;
        }

        $scope.listview = false;
        $http.get(api)
          .success(function(data) {
            $scope.data = data;
            $scope.list = data;
          })
          .error(function(data) {
            // console.log(data);
          });
      };

      // Fires when map loads
        $scope.map = { center: { latitude: 51.5, longitude: -0.1 }, zoom: 11 };
      uiGmapGoogleMapApi.then(function(maps){
        // Default vars
        $scope.list = [];
      });

      // Gets and sets variables upon loading the page
      $scope.$on('$routeChangeSuccess', function (event, current, previous) {
        var url = $location.$$absUrl.split('#')[0];
        $scope.object_id = url.split('/')[4];
        $scope.mode = url.split('/')[3];

        var qs = '?';
        if (current.params.latitude && current.params.longitude) {
          qs = qs + 'latitude=' + current.params.latitude +'&';
          qs = qs + 'longitude=' + current.params.longitude;
        }
        // if (current.params.radius) {
        //   qs = qs + '&radius=' + current.params.radius;
        // };
        if (current.params.id) {
          qs = qs + '&id=' + current.params.id;
        };

        // Fires on page load
        $scope.getData(qs);
        $scope.map = { zoom: 11 };
      });

    }])
})();
