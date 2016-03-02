( function() {
    var myMap, myCircle, app;
    
    app = angular.module('workAround', []);

    app.controller('CoordinatesController', ['$http', '$scope', function($http, $scope){
        var ctrl = this, latitude = 55.76, longtitude = 37.64;
        ctrl.latitude = latitude;
        ctrl.longtitude = longtitude;
        ctrl.radius = 100;
        ctrl.radiuses = [50,100,200];
        ctrl.changeRadius = function() {
            myCircle.geometry.setRadius(ctrl.radius)
        };
        ctrl.submit = function(){
            var response = $http({
                url: "https://api.vk.com/method/photos.search",
                method: 'GET',
                params: {
                    lat: ctrl.latitude,
                    long: ctrl.longtitude,
                    radius: ctrl.radius,
                    count: 100
                }
            });
            response.success(function(data){
                console.log(data);
            });
        };

        ymaps.ready(init);

        function init() {
            myMap = new ymaps.Map("map", {
                center: [latitude, longtitude],
                zoom: 15
            }, {
                searchControlProvider: 'yandex#search'
            });

            myCircle = new ymaps.Circle([
                [latitude, longtitude], ctrl.radius
            ], {}, {
                draggable: true,
            });
            myMap.geoObjects.add(myCircle);
            myCircle.events.add("dragend", function(e){
                var coords = e.get('target').geometry.getCoordinates();
                ctrl.latitude = coords[0];
                ctrl.longtitude = coords[1];
                $scope.$apply();
            });
        }
    }]);

})();