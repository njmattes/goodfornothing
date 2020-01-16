
(function() {
  'use strict';

  var body = d3.select('div')
    , timer
    , i = 0
    , time = 0
  ;

  var change_color = function change_color(color) {
    body.style('background-color', color.color);
  };

  d3.csv('/hal9000portrait/static/csv/hal_rows.csv', function(error, data) {

    var colors = data
      , n = colors.length
    ;

    function repeat() {
      change_color(colors[i]);
      i = i < n - 1 ? i + 1 : 0;
      timer = setTimeout(
        repeat,
        time
      );
    }

    repeat();

  });

})();