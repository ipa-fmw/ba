// Generated by CoffeeScript 1.6.2
(function() {
  define(['backbone'], function(Backbone) {
    var Test;

    return Test = Backbone.Model.extend({
      defaults: {
        error: '',
        collisions: 0,
        date: 0,
        robot: '',
        scenario: '',
        navigation: '',
        testResults: null,
        duration: null,
        distance: null,
        rotation: null
      },
      initialize: function() {
        var date;

        date = this.get('localtime') * 1000;
        return this.set('date', new Date(date));
      }
    });
  });

}).call(this);
