// Generated by CoffeeScript 1.6.2
(function() {
  define(['underscore', 'backbone', 'models/test'], function(_, Backbone, Test) {
    var Tests;

    return Tests = Backbone.Collection.extend({
      model: Test,
      comparator: 'localtime',
      groupBy: function(groups) {
        var groupKey, groupedSiblings, key, model, siblings, _i, _len, _ref;

        groupedSiblings = {};
        groupKey = function(model) {
          var group, key, _i, _len;

          key = '';
          for (_i = 0, _len = groups.length; _i < _len; _i++) {
            group = groups[_i];
            key += model.get(group);
          }
          return key;
        };
        _ref = this.models;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          model = _ref[_i];
          key = groupKey(model);
          siblings = groupedSiblings[key] || (groupedSiblings[key] = []);
          siblings.push(model);
        }
        return _(groupedSiblings).values().map(function(models) {
          return new Tests(models);
        });
      },
      filter: function(filters) {
        var compliedCount, filtered, model, _i, _len, _ref;

        filtered = new Tests;
        compliedCount = 0;
        _ref = this.models;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          model = _ref[_i];
          if (this.allFiltersComply(compliedCount, model, filters)) {
            filtered.add(model, {
              silent: true
            });
            compliedCount++;
          }
        }
        return filtered;
      },
      allFiltersComply: function(number, model, filters) {
        var filter, _i, _len;

        for (_i = 0, _len = filters.length; _i < _len; _i++) {
          filter = filters[_i];
          if (!filter.complies(number, model)) {
            return false;
          }
        }
        return true;
      },
      getIndexesByCid: function() {
        var index, indexesByCid, model, _ref;

        indexesByCid = {};
        _ref = this.models;
        for (index in _ref) {
          model = _ref[index];
          indexesByCid[model.cid] = index;
        }
        return indexesByCid;
      }
    });
  });

}).call(this);
