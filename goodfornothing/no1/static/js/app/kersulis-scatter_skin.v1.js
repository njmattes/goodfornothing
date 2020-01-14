(function(size, number, timer, threshold, network, cg) {
  'use strict';

  let mode = {
    'g': 'gpxl',
    'c': 'cpxl',
  }[cg];

  let width = window.innerWidth;
  let height = window.innerHeight;

  /**
   * Padding multiplier
   * @type {number}
   */
  const padding_m = 0;

  /**
   * Padding surrounding artwork
   * @type {{top: number, left: number, bottom: number, right: number}}
   */
  const padding = {
    top: size * padding_m,
    right: size * padding_m,
    bottom: size * padding_m,
    left: size * padding_m};
  width = Math.ceil(width / size) - (padding.left + padding.right) / size;
  height = Math.ceil(height / size) - (padding.top + padding.bottom) / size;

  const canvas = d3
    .select('main')
    .append('canvas')
    .attr('width', width * size)
    .attr('height', height * size);
  const ctx = canvas.node().getContext('2d');
  ctx.LineCap = 'round';

  function pxls(t) {
    /**
     * If we have run through all pixels, set t back to 0, begin running
     * the wipe() function, and return.
     */
    if (t >= width * height) {
      t = 0;
      wipe(t, width * height);
      return;
    }
    d3.json(`/no1/get_${mode}/${t},${number}/${threshold}/${network}`, {
      headers: {
        'Content-type': 'application/json; charset=UTF-8'
      }}).then(json => {
        for (let i = 0; i < json['pxls'].length; ++i) {
          fill_pxl(
            json.pxls[i].color,
            json.pxls[i].xy
          );
        }
      });
    t += number;
    setTimeout(pxls.bind({}, t), timer);
  }

  async function wipe(t, n) {
    /**
     * Wipe screen clean by increasing R, G, B values to 255 incrementally
     */
    if (n <= 50) {  // If no indexes left to tint
      init_db();
      t = 0;
      pxls(t);
      return;
    }
    if (t >= n) {  // If current index in loop is >= indexes left to tint
      t = 0;  // Start back at 0
    }
    let json = await d3.json(`/no1/get_half_pxls/${t},${number}/${threshold}/${network}`, {
      headers: {'Content-type': 'application/json; charset=UTF-8'}});
    for (let i = 0; i < json['pxls'].length; ++i) {
      fill_pxl(
        json.pxls[i].color,
        json.pxls[i].xy
      );
    }
    n = json.n;
    t += number;
    setTimeout(wipe.bind({}, t, n), timer);
  }

  const fill_pxl = function fill_pxl(rgb, xy) {
    ctx.fillStyle = `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, 1)`;
    ctx.beginPath();
    ctx.rect(xy[0] * size, xy[1] * size, size, size);
    ctx.fill();
  };

  async function init_db() {
    let json = await d3.json(`/no1/init/${width}/${height}`,
      {headers: {'Content-type': 'application/json; charset=UTF-8'}});
    if (json.success) {
      console.log('db initialized');
      pxls(0);
    }
  }

  init_db();

})(size, number, timer, threshold, network, cg);