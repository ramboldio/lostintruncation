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

## Hooking up the Thermal Printer to the Raspberry Pi
!(https://cdn-learn.adafruit.com/assets/assets/000/063/083/small360/components_pi_thermal_printer_uart_bb.png?1538760194)


## Install Raspi Access Point
```
curl -sL https://install.raspap.com | bash
```
