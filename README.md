# Good-for-nothing

The Good-for-nothing project by [Nicholas Kersulis](http://kersulis.com)
and [Nathan](http://skeptic.ist) [Matteson](http://obstructures.org)
lives at [goodfornothing.pictures](https://goodfornothing.pictures).

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


## Local installation

The project has few dependencies. Caching depends on `redis` which can be
installed `brew install redis` on OS X or `apt-get install redis-server`
(or similar depending on your package manager) on many *nix boxes.
It also depends on MongoDB which is slightly trickier to install. Instructions
for installing the open source Community edition on most platforms can be found
here: [docs.mongodb.com/manual/administration/install-community/]
(https://docs.mongodb.com/manual/administration/install-community/).

The easiest way to install Good-for-nothing locally on your own machine,
for viewing or for further development, is to checkout the repo:

```
git clone http://github.com/njmattes/goodfornothing
cd goodfornothing
```

The web service is built in python atop `flask`. Other common packages used
include `numpy`, `scikit-learn`, and `imageio`. Required python packages
can be installed simply by issuing:

```
pip install -r requirements.txt
```

Launching the service cab done with

```
python run.py
```

## Set up to run from a Raspberry Pi

Good-for-nothing can be projected using a Raspberry Pi (or other similar
computing platform). The instructions below are for setting up a
'headless' Pi (no monitor, no keyboard) that can drive a projector
and will start the goodfornothing app and the Chromium browser upon
reboot.

### Set up a 'headless' Raspberry Pi Zero

1. Download [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)

2. Insert a MicroSD (at least 8GB).

3. Find the MicroSD:

```
sudo df -h
```

4. Unmount the disk, replacing `X` and `Y` with the proper digits
   found in step 1.:

```
sudo diskutil unmountDisk /dev/diskXsY
```

5. Copy the image:

```
sudo dd bs=1m \
  if=/path/to/raspbian.img \
  of=/dev/rdiskX
```

6. Add an `ssh` file to the root of the Raspbian install:

```
touch /Volumes/boot/ssh
```

7. Add an `avahi` file to the root of the Raspbian install:

```
touch /Volumes/boot/avahi
```

8. Add to the bottom of the `config.txt` file:

```
echo 'dtoverlay=dwc2' >> /Volumes/boot/config.txt
```

9. Add to the `cmdline.txt` file

```
sed
  -e 's/ rootwait / rootwait modules-load=dwc2,g_ether /'
  -i ''
  /Volumes/boot/cmdline.txt
```

10. To autostart the application:

```
echo '/usr/bin/chromium-browser --kiosk --ignore-certificate-errors --disable-restore-session-state https://www.google.com' >> /etc/xdg/lxsession/LXDE-pi/autostart
```

Install required packages:

1. Log into the Raspberry Pi connected by USB.

```
ssh pi@raspberry.local
```

2. Install required packages.

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install redis
sudo apt-get install mongodb
```

3. Make a directory for the project and clone the repo.

```
mkdir /var/www
cd /var/www
git clone https://github.com/njmattes/goodfornothing
git checkout develop
sudo pip3 install -r goodfornothing/requirements.txt
```

4. Set up auto execution.

```
sudo chmod 0775 /var/www/goodfornothing/pi.sh
sudo crontab -e

# Add these lines to cron.
# @reboot sh /var/www/goodfornothing/pi.sh >/home/pi/goodfornothing.log 2>&1
# @reboot /usr/bin/chromium-browser --kiosk --ignore-certificate-errors --disable-restore-session-state https://127.0.0.1:5000/no1
```
