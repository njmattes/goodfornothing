
(function() {
  'use strict';

  d3.json('/selfie1/static/json/tiananmen_selfie_400x300_2.json', function(data) {

    console.log(data);

    var body = d3.select('body')
      , canvas = d3.select('body').append('canvas')
        .attr('width', 400)
        .attr('height', 300)
      , context = canvas.node().getContext('2d')
      , time = data.idx[1]/30
      , timer
      , n = data.idx.length
      , i = 0
      , pixels = []
      , max_idx_a = d3.max(d3.entries(data.ab), function(d) {
        return d['value'].length > 0 ? d['key'] : 0 })
    ;

    console.log(data.a);
    console.log(data.idx.length);

    var draw_pixels = function draw_pixels() {
      pixels = data.a[data.idx[i].toFixed(1)].concat(
        data.b[data.idx[i].toFixed(1)]
      );
      for (var p = 0; p < pixels.length; ++p) {
        context.beginPath();
        context.rect(pixels[p][1], pixels[p][0], 1, 1);
        context.fillStyle='rgb('+pixels[p][2].join(',')+')';
        context.fill();
        context.closePath();
      }
    };

    var repeat = function repeat() {
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