
## Good-for-nothing (no. 1) interface

Good-for-nothing (no. 1) has a simple URL-based interface for viewers
who want to explore the work beyond its default grayscale state. The API
is a hot mess right now (Oct 2020), but is more-or-less built around
alternating key-value pairs separated by slashes. The easiest way to ensure
its functionality is to include all key-value pairs in the following order:

```
goodfornothing.pictures/color/<c|g>/size/<int>/number/<int>/timer/<int>/threshold/<int>/network/<int>')
```

`color/c` switches from greyscale to color. Colors are currently not
customizable. Defaults to `g` for greyscale pixels.

`size/<int>` determines the size of the pixels. Defaults to `20`.

`number/<int>` determines the batch size of 'pixels' that are drawn during
a single frame of the animation. Defaults to `10`.

`timer/int` determines the temporal delay in milliseconds between
frames. Defaults to `20` milliseconds.

The reciprocal of `threshold/int` determines the point at which the animation
switches from placing randomly colored pixels on the canvas to coloring
each pixel according to its closest neighbors. E.g. a threshold of 2 would
cause 1/2 of the screen to be random, and the latter half of the pixels to be
averaged. Defaults to `30` (1/30th of the screen is randomized before smoothing).

`network/<int>` determines the number of neighboring pixels to use to
average the colors after `threshold` has been met. Defaults to `3`.

`number` and `timer` primarily affect the speed of the animation---both
its framerate and the length of time it takes to complete a cycle of
drawing and erasure.

`threshold` and `network` affect the quality of the 'surface' that is drawn.

Future parameters will be included one day, and the API will eventually be
made more robust.
