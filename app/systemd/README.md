```bash
cd /home/rpi/repos/pi-rgb-sign
sudo cp app/systemd/rgb-sign.service /etc/systemd/system
cd /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl stop rgb-sign.service
sudo systemctl start rgb-sign.service
sudo systemctl enable rgb-sign.service
```