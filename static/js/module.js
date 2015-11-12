var app = angular.module('QKDiary', ['ngAnimate', 'ngResource', 'ngCookies', 'ui.bootstrap', 'ui.router', 'angularMoment', 'xeditable']);

app.run(function(editableOptions, editableThemes) {
  editableThemes.bs3.inputClass = 'input-sm';
  editableThemes.bs3.buttonsClass = 'btn-sm';
  editableOptions.theme = 'bs3';
});
