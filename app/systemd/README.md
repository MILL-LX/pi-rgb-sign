```bash
cd /home/rpi/repos/pi-rgb-sign
sudo cp app/systemd/pi-rgb-sign.service /etc/systemd/system
cd /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl stop pi-rgb-sign.service
sudo systemctl start pi-rgb-sign.service
sudo systemctl enable pi-rgb-sign.service
```
