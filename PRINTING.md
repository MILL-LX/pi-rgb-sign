# This requires a local installation of the Linux CUPS package.
#   sudo apt update
#   sudo apt install cups

After installing CUPS, you can start and enable the CUPS service:

```bash
sudo systemctl start cups
sudo systemctl enable cups
```

You can then access the CUPS web interface at http://your-raspberry-pi-ip:631.