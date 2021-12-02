(function() {
  /*
   Good-for-nothing (pours no. 2) [2021]
   */

  'use strict';

  const timer = 300;
  const size = 40;

  let width = window.screen.width;
  let height = window.screen.height;

  /**
   * Padding surrounding artwork
   * @type {{top: number, left: number, bottom: number, right: number}}
   */
  width = Math.ceil(width / 2 / size) * 2;
  height = Math.ceil(height / 2 / size) * 2;

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

  // The probability of a pixel being non-empty
  const n0 = 0.02;

  let tested = 0;

  // idxs hold values 0 or 1 indicating the presence of a colored pixel.
  // arrs hold color data from 0 to 255.
  // One idx and one arr for each channel.
  // arbX arrays hold the previous layers (for mixing)
  let idxr = math.reshape(math.zeros(height * width), [height, width]);
  let idxg = math.reshape(math.zeros(height * width), [height, width]);
  let idxb = math.reshape(math.zeros(height * width), [height, width]);
  let arrr = math.reshape(math.zeros(height * width), [height, width]);
  let arrg = math.reshape(math.zeros(height * width), [height, width]);
  let arrb = math.reshape(math.zeros(height * width), [height, width]);
  let arbr = math.reshape(math.zeros(height * width), [height, width]);
  let arbg = math.reshape(math.zeros(height * width), [height, width]);
  let arbb = math.reshape(math.zeros(height * width), [height, width]);



  const get_previous_row = function get_previous_row(idxs, idx) {
    /**
     * Get previous row of indexes
     */
    return math.squeeze(
      math.subset(idxs, math.index(idx - 1, math.range(0, width)))
    );
  }

  const get_nonwhite_idxs = function get_nonwhite_idxs(previous) {
    /**
     * Given a row of pixels return the indices of the non zero pixels.
     * @type {number[]}
     */
    let non_white_idxs = [];
    math.forEach(
      previous,
      // NOTE: In the callback below, i is an array not an integer,
      function(d, i) { if (d > 0) { non_white_idxs.push(i[0]); } });
    return non_white_idxs
  }

  const new_pixel_probability = function new_pixel_probability(idx) {
    /**
     * The probability of a pixel in a new row being empty or not.
     * @type {number}
     */
    const probability = .5 ** (idx / height);
    return [probability, 1 - probability]
  };

  const mean_without_zeros = function mean_without_zeros(arr) {
    /**
     * Calculate the mean of the columns of a matrix ignoring zero values.
     * This is a bad implementation of np.nanmean()
     * @type number
     */
    const filt = arr.filter(d => d !== 0);
    if (filt.length === 0) {
      return 0;
    }
    const sum = filt.reduce((a, b) => a + b);
    const mean = sum / filt.length;
    return mean;
  }

  const get_hues = function get_hues(arr, idx, idxs, arb) {
    /**
     * Determine the hues for a single channel of a single row.
     * Note that the idx argument must be >= 1.
     */
    let row = math.subset(arr, math.index(idx-1, math.range(0, width)));

    // Create three stacked rows. One has the channel value in the pixel above,
    // one the pixel to the left, the other to the right.
    let hues = math.concat(
      row.reshape([1, width]),
      math.map(row, function(d, i, m) {
        return i[1] > 0
          ? math.subset(m, math.index(i[0], i[1]-1))
          : math.subset(m, math.index(i[0], width-1))
      }).reshape([1, width]),
      math.map(row, function(d, i, m) {
        return i[1] === width - 1
          ? math.subset(m, math.index(i[0], 0))
          : math.subset(m, math.index(i[0], i[1]+1))
      }).reshape([1, width]),
      0
    );

    // For each pixel, average the three channel values above
    hues = math.apply(hues, 0, mean_without_zeros)

    // For each pixel randomly move the channel by 2
    hues = math.map(hues, function(d) {
      return d === 0
        ? 0
        : d + math.pickRandom([0, 5])
    });

    // I think this is turning off a small amount of random pixels in the row.
    arr.subset(
      math.index(idx, math.range(0, width)),
      math.dotMultiply(
        hues,
        math.squeeze(math.subset(idxs, math.index(idx, math.range(0, width))))
      )
    )

    return hues;

  };

  const paint_first_row = function paint_first_row(ridx, idxs, arr) {
    /**
     * Create the first row.
     */
    let mask = math.zeros(width);
    while (math.sum(mask) === 0) {
      mask = math.random([width]);
      math.forEach(mask, function(d, i, arr) { arr[i] = d < n0 ? 1 : 0; });
    }
    idxs.subset(ridx, mask);
    let hues = math.dotMultiply(
      math.subset(idxs, ridx),
      math.randomInt([1, width], 0, 191));

    arr.subset(ridx, hues);

    return hues;

  };

  const fill_pxl = function fill_pxl(rgb, xy) {
    /**
     * Paint a pixel on the <canvas>
     * @type {string}
     */
    // ctx.fillStyle = `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, 1)`;
    ctx.fillStyle = rgb;
    ctx.beginPath();
    ctx.rect(xy[0] * size, xy[1] * size, size, size);
    ctx.fill();
  };

  const make_row = function make_row(idx, idxs, arr, arb) {
    /**
     * Create idxs and arrs for a single row and paint it.
     */

    const ridx = math.index(idx, math.range(0, width));
    const new_pxl_prob = new_pixel_probability(idx);

    if (idx === 0) {

      return paint_first_row(ridx, idxs, arr);

    } else {

      let previous = get_previous_row(idxs, idx);
      let non_white_idxs = get_nonwhite_idxs(previous);
      // Random walk as the pixels descend
      let movement = math.randomInt([non_white_idxs.length], -2, 2);
      let new_idxs = math.add(non_white_idxs, movement);

      // Clamp pixels to row with
      // TODO! Port this to old pours
      new_idxs = math.map(new_idxs, function (d) {
        return d >= width
          ? width - 1
          : d < 0
            ? 0
            : d;
      });

      if (new_idxs.length > 0) {
        idxs.subset(
          math.index(idx, math.squeeze(new_idxs)),
          math.squeeze(math.ones(new_idxs.length)));
      }

      let new_row = math.map(
        math.subset(idxs, ridx),
        function (d, i, m) {
          return d === 0 ? math.pickRandom([0, 1], new_pxl_prob) : d;
        });

      idxs.subset(ridx, new_row);

      return get_hues(arr, idx, idxs, arb);

    }

  };

  const blend_row = function blend_row(idx, hues) {

    const ridx = math.index(idx, math.range(0, width));

    for (let j = 0; j < width; ++j) {

      const jidx = math.index(idx, j);

      let under_color = d3.rgb(
        255 - arbr.subset(jidx),
        255 - arbg.subset(jidx),
        255 - arbb.subset(jidx),
      );

      let over_color = d3.rgb(
        255 - arrr.subset(jidx),
        255 - arrg.subset(jidx),
        255 - arrb.subset(jidx),
      );

      const under_color_hsl = d3.hsl(over_color);

      const over_color_hsl = d3.hsl(under_color);

      under_color.opacity = (1 - under_color_hsl.l);
      over_color.opacity = (1 - over_color_hsl.l);

      let new_color = under_color + '';

      if (over_color.r + over_color.g + over_color.b < 255 * 3) {
        new_color = d3.lab(d3.interpolateLab(
          over_color,
          under_color
        )(.5)).darker((1 - under_color_hsl.l) * 10) + '';
      }

      fill_pxl(new_color, [j, idx]);

    }

    arbr.subset(ridx, math.subset(arrr, ridx));
    arbg.subset(ridx, math.subset(arrg, ridx));
    arbb.subset(ridx, math.subset(arrb, ridx));

  };

  const draw = function draw(t, idx) {
    /**
     * Bootstraps the drawing. Iterates through each channel. Creates a row
     * for each channel. Then calls itself again. When it fills the height,
     * it starts over at 0.
     */

    // let hues = math.reshape(math.zeros(height * width * 3), [height, width, 3]);
    let hues = math.matrix([]);

    let empty_channels = 0;

    for (let [idxs, arr, arb] of [
      [idxr, arrr, arbr], [idxg, arrg, arbg], [idxb, arrb, arbb]
    ]) {

      // hues = math.concat(hues, make_row(idx, idxs, arr, arb));
      make_row(idx, idxs, arr, arb);

    }

    blend_row(idx, hues);

    ++idx;



    if (idx === height) {
      idx = 0;
      idxr = math.reshape(math.zeros(height * width), [height, width]);
      idxg = math.reshape(math.zeros(height * width), [height, width]);
      idxb = math.reshape(math.zeros(height * width), [height, width]);
    }

    setTimeout(draw.bind({}, t, idx), timer);

  }

  draw(timer, 0);

})();
