# LostInTruncation Exhibit Ars Electronica Garden Berlin 

## Installation & Running
```
make intstall 
make up
```

## Architecture

web app <--- WiFi/REST ---> Server <--- CUPS ---> photo printer
				^------ SERIAL -> receipt printer

## Install Raspi Access Point
```
curl -sL https://install.raspap.com | bash
```
