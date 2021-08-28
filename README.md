# LostInTruncation Exhibit Ars Electronica Garden Berlin 

## Installation & Running
```
make intstall 
make thermal_printer_work
make up
```

thermal printer stuff is from here: https://github.com/adafruit/Python-Thermal-Printer
restart may be a good idea after installation

## Architecture
```
web app <--- WiFi/REST ---> Server <--- CUPS ---> photo printer
				^------ SERIAL -> receipt printer
```

## Install Raspi Access Point
```
curl -sL https://install.raspap.com | bash
```
