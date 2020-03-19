# Good-for-nothing

Code for the Good-for-nothing project by Nicholas Kersulis and Nathan Matteson,
found at [goodfornothing.pictures](https://goodfornothing.pictures).

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