# RASPRINTER

## Raspbian configuration to manage:
## - Scanner (with SANE)
## - Printer (with CUPS)
## - 3D Printer (with OCTOPRINT)


### SCANNER
```
sudo apt-get install sane
sudo apt-get install sane-utils

Add the following line in fstab
//raspberrypi3/TOSHIBA_EXT  /media/backup  cifs  guest  0  0

copy scan.bash in the /home/pi/ directory
sudo chmod +x scan.bash

sudo apt-get install imagemagick
apt-get install python-rpi.gpio

copy button_led.py in the /home/pi/ directory

sudo crontab -e
add -> @reboot /usr/bin/python /home/pi/button_led.py
```



### PRINTER

```
sudo apt-get install cups
sudo usermod -a -G lpadmin pi
sudo nano /etc/cups/cupsd.conf
change: "Listen localhost:631" -> "Port 631"
add 3 times "Allow @local"  1 in # Restrict access to the server... 1 in # Restrict access to the admin pages... and 1 in # Restrict access to the configuration files...
apt-get install hplip
sudo /etc/init.d/cups restart

sudo hp-setup -i
```

Visit: https://192.168.1.86:631/   Administration  / add printer


### 3D PRINTER

```
cd ~
sudo apt update
sudo apt install python-pip python-dev python-setuptools python-virtualenv git libyaml-dev build-essential
mkdir OctoPrint && cd OctoPrint
virtualenv venv
source venv/bin/activate
pip install pip --upgrade
pip install octoprint

sudo usermod -a -G tty pi
sudo usermod -a -G dialout pi

wget https://github.com/foosel/OctoPrint/raw/master/scripts/octoprint.init && sudo mv octoprint.init /etc/init.d/octoprint
wget https://github.com/foosel/OctoPrint/raw/master/scripts/octoprint.default && sudo mv octoprint.default /etc/default/octoprint
sudo chmod +x /etc/init.d/octoprint

make sure your /etc/default/octoprint is modified like this:
DAEMON=/home/pi/OctoPrint/venv/bin/octoprint

sudo update-rc.d octoprint defaults
```




