(function() {
  'use strict';

  const hal_eye = d3.select('div');
  const CSV_URL = '/hal9000portrait/static/csv/hal_rows.csv';
  let timer;
  let i = 0;
  let time = 0;

  const change_color = function change_color(color) {
    hal_eye.style('background-color', color.color);
  };

  d3.csv(CSV_URL, function(error, data) {

    const COLORS = data;
    const N = COLORS.length;

    function repeat() {
      change_color(COLORS[i]);
      i = i < N - 1 ? i + 1 : 0;
      timer = setTimeout(
        repeat,
        time
      );
    }

    repeat();

  });

})();