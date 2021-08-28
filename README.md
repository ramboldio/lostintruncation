# LostInTruncation Exhibit Ars Electronica Garden Berlin 

## Installation & Running
```
make intstall 
make thermal_printer_work
make up
```

thermal printer stuff is from here: https://github.com/adafruit/Python-Thermal-Printer
restart may be a good idea after installation

Make sure to set the `COLABURL` environment variable to the correct endpoint where the image generation happens

## Architecture
```
			 	/----- HTTP ----> Image & Text Generation (CoLab)
web app <--- HPPT -------> Server <--- CUPS ----> photo printer
				^ ^--- CUPS ----> receipt printer (for images)
				 \---- SERIAL --> receipt printer (for text)
```

## Hooking up the Thermal Printer to the Raspberry Pi
![](https://cdn-learn.adafruit.com/assets/assets/000/063/083/small360/components_pi_thermal_printer_uart_bb.png?1538760194)


## Install Raspi Access Point
```
curl -sL https://install.raspap.com | bash

```
