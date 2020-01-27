(function(OPTIONS) {
  'use strict';

  const WIDTH = document.body.clientWidth;
  const HEIGHT = document.body.clientHeight;
  const M = Math.floor(WIDTH / OPTIONS.size) - 1;
  const N = Math.floor(HEIGHT / OPTIONS.size) - 1;
  const xs = Array.from(Array(M),
    (d, index) => index * OPTIONS.size +
      (WIDTH - (M - 1) * OPTIONS.size) / 2);
  const ys = Array.from(Array(N),
    (d, index) => index * OPTIONS.size +
      (HEIGHT - (N - 1) * OPTIONS.size) / 2);
  console.log(xs, ys);

  const context = d3.select('main')
    .append('canvas')
    .attr('width', WIDTH)
    .attr('height', HEIGHT)
    .node()
    .getContext('2d');

  const time = 300;

  const pick_different_random_point = function pick_different_random_point(points) {
    for (let i = 0; i < points.length; ++i) {
      for (let j = 0; j < 2; ++j) {
        if (points[i][j] === 0) {
          points[i][j] += Math.floor(Math.random() * 2)
        } else if (j === 0 && points[i][j] === M) {
          points[i][j] -= Math.floor(Math.random() * 2)
        } else if (j === 1 && points[i][j] === N) {
          points[i][j] -= Math.floor(Math.random() * 2)
        } else {
          points[i][j] += (1 - Math.floor(Math.random() * 3))
        }
      }
    }
    return points;
  };

  const pick_initial_points = function pick_initial_points() {
    return [
      [ Math.floor(Math.random() * M / 2),
        Math.floor(Math.random() * N / 2) ],
      [ Math.floor(Math.random() * M / 2),
        Math.floor(Math.random() * (N - N / 2) + N / 2) ],
      [ Math.floor(Math.random() * (M - M / 2) + M / 2),
        Math.floor(Math.random() * (N - N / 2) + N / 2)],
      [ Math.floor(Math.random() * (M - M / 2) + M / 2),
        Math.floor(Math.random() * N / 2)],
    ];
  };

  const draw_polygon = function draw_polygon(points) {
    context.fillStyle = 'rgba(0, 0, 0, .1)';
    context.beginPath();
    context.moveTo(xs[points[0][0]], ys[points[0][1]]);
    for (let i = 1; i < points.length; ++i) {
      context.lineTo(xs[points[i][0]], ys[points[i][1]]);
    }
    context.closePath();
    context.fill();
  };

  let points = pick_initial_points();

  const repeat = function repeat() {

    draw_polygon(points);
    points = pick_different_random_point(points);

    let timer = setTimeout(
      repeat,
      time,
    );

  };

  repeat();

})(OPTIONS);
