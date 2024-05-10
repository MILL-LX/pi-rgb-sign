# Systemd Service Installation

This application can start up automatically on reboot of your Raspberry Pi. Use the following commands to install the service, start the application, and enable it to start up on reboot:


```bash
cd /home/rpi/repos/pi-rgb-sign
sudo cp app/systemd/pi-rgb-sign.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl stop pi-rgb-sign.service
sudo systemctl start pi-rgb-sign.service
sudo systemctl enable pi-rgb-sign.service
```
