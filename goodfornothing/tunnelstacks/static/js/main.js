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

  const canvas = d3.select('main')
    .append('canvas')
    .attr('width', WIDTH)
    .attr('height', HEIGHT);
  const ctx = canvas
    .node()
    .getContext('2d');

  let points;

  const pick_different_random_point = function pick_different_random_point(points) {
    for (let i = 0; i < points.length; ++i) {
      for (let j = 0; j < 2; ++j) {
        if (points[i][j] === 0) {
          // Points on left edge or top
          points[i][j] += Math.floor(Math.random() * 2)
        } else if (j === 0 && points[i][j] === M - 1) {
          // Point on right
          points[i][j] -= Math.floor(Math.random() * 2)
        } else if (j === 1 && points[i][j] === N - 1) {
          // Point on bottom
          points[i][j] -= Math.floor(Math.random() * 2)
        } else {
          points[i][j] += (Math.floor(Math.random() * 3) - 1)
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

  const get_point_from_indices = function get_point_from_index(idx) {
    return [
      xs[points[idx][0]],
      ys[points[idx][1]]
    ];
  };

  const draw_polygon = function draw_polygon(points) {
    ctx.fillStyle = OPTIONS.fg;
    ctx.beginPath();
    let pt = get_point_from_indices(0);
    console.log(pt);
    ctx.moveTo(pt[0], pt[1]);
    for (let i = 1; i < points.length; ++i) {
      let pt = get_point_from_indices(i);
      console.log(pt);
      ctx.lineTo(pt[0], pt[1]);
    }
    ctx.closePath();
    ctx.fill();
  };

  const init = function init() {
    points = pick_initial_points();
    console.log(points);
    ctx.fillStyle = OPTIONS.bg;
    console.log(canvas.width);
    ctx.fillRect(0, 0, canvas.node().width, canvas.node().height);
  };

  const repeat = function repeat() {
    draw_polygon(points);
    points = pick_different_random_point(points);

    let timer = setTimeout(
      repeat,
      OPTIONS.time,
    );
  };

  init();
  repeat();

})(OPTIONS);
