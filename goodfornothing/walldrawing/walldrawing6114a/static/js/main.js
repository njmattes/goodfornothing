(function() {
  'use strict';

  const JSON_PATH = '/walldrawing6114a/static/json/venice_6114_serial.json';
  const WALL_DIR = '/walldrawing6114a/static/png/serial_walls/';
  const TIMER = 100;

  let n;

  const wall = d3.select('main')
    .append('img')
    .attr('class', 'wall');

  const replace_image = function replace_image(walls, i) {
    console.log(i);
    wall.attr('src', WALL_DIR + walls[i % n]);
    i = i > n ? 0 : i + 1;
    setTimeout(replace_image.bind({}, walls, i), TIMER);
  };

  const init = async function init() {
    let json = await d3.json(JSON_PATH,
      {headers: {'Content-type': 'application/json; charset=UTF-8'}});
    if (json.walls) {
      n = json.walls.length;
      replace_image(json.walls, 0)
    }
  };

  init();

})();