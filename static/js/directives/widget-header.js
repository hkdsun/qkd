/**
 * Widget Header Directive
 */

angular
    .module('QKDiary')
    .directive('rdWidgetHeader', rdWidgetTitle);

function rdWidgetTitle() {
    var directive = {
        requires: '^rdWidget',
        scope: {
            title: '@',
            icon: '@'
        },
        transclude: true,
        template: '<div class="widget-header">' +
                    '<div class="row" ng-transclude>' +
                    '</div>' +
                  '</div>',
        restrict: 'E'
    };
    return directive;
};
