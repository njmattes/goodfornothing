(function() {
  'use strict';

  const t = 100;
  const timer = 1000;
  const size = 10;

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
  width = Math.ceil(width / 2 / size) * 2;
  height = Math.ceil(height / 2 / size) * 2 + 1;

  /**
   * Add <canvas> to <main> with width and height attributes set to
   * fill the screen. Save context and set lineCap.
   */
  const canvas = d3
    .select('main')
    .append('canvas')
    .attr('width', width * size)
    .attr('height', height * size);
  const ctx = canvas.node().getContext('2d');
  ctx.LineCap = 'round';

  d3.json(`/horizon/static/js/app/horizon.json`, {
    headers: {
      'Content-type': 'application/json; charset=UTF-8'
    }}).then(json => {

      const sea = math.matrix(json.sea);
      const sky = math.matrix(json.sky);
      const colors = json.colors;
      const horiz = math.matrix(json.horizon);

      const draw = function draw(t) {
        // Draw no2
        let h = [];
        for (let i = 0; i < width; ++i) {
          let hue_idx = get_hue_idx(horiz);
          fill_pxl(
            get_rgb_from_idx(hue_idx, colors),
            [i, Math.ceil(height/2)]);
          h.push(hue_idx);
        }
        // Store no2 in tensor
        let picture_plane = [h];

        // Draw sky and sea
        for (let i = 0; i < height/2; ++i) {

          let sea_idxs = picture_plane[picture_plane.length-1];
          let sky_idxs = picture_plane[0];

          for (let j = 0; j < width; ++j) {

            let a = j - 2, b = j - 1, c = j, d = j + 1, e = j + 2;
            if (j === 0) {
              a = e; b = d;
            } else if (j === 1) {
              a = b;
            } else if (j === width - 1) {
              d = b; e = a;
            } else if (j === width - 2) {
              e = d;
            }
            for (const [probability, idxs, y_offset]
              of [[sea, sea_idxs, i], [sky, sky_idxs, -i]]) {
              let slice = math.index(
                idxs[a], idxs[b], idxs[c], idxs[d], idxs[e],
                math.range(0, 16)
              )
              let hue_idx = get_hue_idx(
                math.flatten(math.subset(probability, slice)));
              fill_pxl(
                get_rgb_from_idx(hue_idx, colors),
                [j, Math.ceil(height/2 + y_offset)]);

            }
          }
        }
      }

      function redraw(t) {

        setTimeout(redraw.bind({}, t), timer);
      }

      draw();
      redraw(10000)

    });

  const fill_pxl = function fill_pxl(rgb, xy) {
    ctx.fillStyle = `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, 1)`;
    ctx.beginPath();
    ctx.rect(xy[0] * size, xy[1] * size, size, size);
    ctx.fill();
  };

  const get_idx = function get_idx(a, b, c, d, e) {
    return a*16**5 + b*16**4 + c*16**3 + d*16**2 + e*16;
  };

  const get_hue_idx = function get_hue_idx(probability) {
    let rnd = Math.random();
    return argmax(reciprocal(math.subtract(cumsum(probability), rnd)));
  }

  const get_rgb_from_idx = function get_rgb_from_idx(hue_idx, colors) {
    return colors[hue_idx]
  }

  const cumsum = function cumsum(arr) {
    return math.map(arr, function (x, i, a) {
      return math.sum(math.subset(a, math.index(math.range(0, i[0]+1))));
    })
  }

  const reciprocal = function reciprocal(arr) {
    return math.map(arr, function (x, i, a) {
      return 1 / x;
    })
  }

  const argmax = function argmax(arr) {
    return arr.toArray().indexOf(math.max(arr))
  }

})();
