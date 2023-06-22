# usbautofan
USB Fan Automation for Raspberry Pi

## Hardware Requirements
* Raspberry Pi
* USB Fan (I used a CPU fan with a 3pin to USB adapter)

## Software Requirements
* If you're using a Raspberry 4, make sure your bootloader is at least on version 00137ad
   - To check, run `sudo rpi-eeprom-update` and to update run `sudo rpi-eeprom-update -d -a`
* `apt-get install build-essential`
* [Python3](https://projects.raspberrypi.org/en/projects/generic-python-install-python3#linux)
* [uhubctl](https://github.com/mvp/uhubctl)

## Setup
### Targeting
Firstly, we need to figure out which port we need to address with uhubctl. There is some info in the [uhubctl documentation](https://github.com/mvp/uhubctl#raspberry-pi-4b) and we can do some testing:

Make sure the fan is connected and reboot to be sure. Fan should be running.
Run `uhubctl` to list all USB hubs and ports. The syntax for uhubctl is `uhubctl -l [hub] -p [port] -a [action]`, try out some hubs (e.g. 2 or 1-1) and ports (1-4) with action 0 (off) until your fan turns off but (if applicable) other USB devices still work.

For reference, I'm using a Raspberry Pi 4B and have the Fan connected to the lower USB2 port. As per the uhubctl documentation, my command is `uhubctl -l 1-1 -a 0`.

If that command works for you, you don't need to change anything in the python script. If you need another command, make sure to change line 23 in the code accordingly.

### Installation
1. Download `usbautofan.py` and place it in `/root/usbautofan/`
   - Change uhubctl command if needed (see Targeting section)
   - (Optional) If you want to, you can change the maxtemp and mintemp variables. The numbers are degrees C without decimals. maxtemp determines when the Fan will turn on while mintemp will determine when it turns off.
2. Run `sudo nano /etc/systemd/system/usbautofan.service` and paste this:
```
[Unit]
Description=USB Fan Automation
After=mult-user.target

[Service]
ExecStart=/usr/bin/env python3 /root/usbautofan/usbautofan.py

[Install]
WantedBy=multi-user.target
```
3. Refresh Daemon and enable the service:
```
sudo systemctl daemon-reload
sudo systemctl enable usbautofan.service
```
4. Check if it's running:
```
systemctl status timestamp.service
```
