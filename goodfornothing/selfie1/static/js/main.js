(function() {
  'use strict';

  const JSON_URL = '/selfie1/static/json/tiananmen_selfie_400x300_2.json';
  const WIDTH = 400;
  const HEIGHT = 300;
  const PIXEL = 2;

  let time;
  let timer;
  let n;

  const context = d3.select('main')
    .append('canvas')
    .attr('width', WIDTH * PIXEL)
    .attr('height', HEIGHT * PIXEL)
    .node()
    .getContext('2d');

  const draw_pixel = function draw_pixel(x, y, rgb) {
    context.beginPath();
    context.rect(x * PIXEL, y * PIXEL, PIXEL, PIXEL);
    context.fillStyle='rgb('+rgb.join(',')+')';
    context.fill();
    context.closePath();
  };

  const draw_pixels = function draw_pixels(json, i) {

    let pixels = json.a[json.idx[i]].concat(json.b[json.idx[i]]);

    for (let p = 0; p < pixels.length; ++p) {
      let pixel = pixels[p];
      draw_pixel(pixel[1], pixel[0], pixel[2]);
    }

  };

  const repeat = function repeat(json, i) {

    draw_pixels(json, i);

    timer = setTimeout(
      repeat,
      time,
      json,
      (i + 1) % n
    );

  };

  d3.json(JSON_URL, {
    headers: {

      'Content-type': 'application/json; charset=UTF-8'

    }}).then(json => {

      n = json.idx.length;
      time = json.idx[1] / 30;
      repeat(json, 0);

  });

})();
