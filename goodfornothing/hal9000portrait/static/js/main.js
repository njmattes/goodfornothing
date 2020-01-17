(function() {
  'use strict';

  const hal_eye = d3.select('div');
  const CSV_URL = '/hal9000portrait/static/csv/hal_rows.csv';
  let timer;
  let time = 0;
  let n;

  const change_color = function change_color(row) {
    hal_eye.style('background-color', row.color);
  };

  const repeat = function repeat(json, i) {
      change_color(json[i]);
      timer = setTimeout(
        repeat,
        time,
        json,
        (i + 1) % n
      );
    };

  d3.csv(CSV_URL, {
    headers: {
      'Content-type': 'application/json; charset=UTF-8'
    }}).then(json => {
      n = json.length;
      repeat(json, 0);
    });

})();