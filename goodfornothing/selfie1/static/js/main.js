(function() {
  'use strict';

  const JSON_URL = '/selfie1/static/json/tiananmen_selfie_400x300_2.json';
  const WIDTH = 400;
  const HEIGHT = 300;
  const PIXEL = 2;

  d3.json(JSON_URL, function(error, data) {

    const canvas = d3.select('main')
      .append('canvas')
      .attr('width', WIDTH * PIXEL)
      .attr('height', HEIGHT * PIXEL);
    const context = canvas.node().getContext('2d');
    let time = data.idx[1] / 30;
    let timer;
    let i = 0;
    let pixels = [];
    let max_idx_a = d3.max(d3.entries(data.ab), function(d) {
        return d['value'].length > 0 ? d['key'] : 0 });

    const draw_pixels = function draw_pixels() {
      pixels = data.a[data.idx[i]].concat(data.b[data.idx[i]]);
      for (let p = 0; p < pixels.length; ++p) {
        context.beginPath();
        context.rect(pixels[p][1] * PIXEL, pixels[p][0] * PIXEL,
          PIXEL, PIXEL);
        context.fillStyle='rgb('+pixels[p][2].join(',')+')';
        context.fill();
        context.closePath();
      }
    };

    const repeat = function repeat() {
      draw_pixels(pixels);
      i++;
      if (i >= data.idx.length) {
        i = 0;
      }
      timer = setTimeout(
        repeat,
        time
      );
    };

    repeat();

  });

})();
