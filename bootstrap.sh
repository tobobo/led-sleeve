sudo cp -v /home/pi/led-sleeve/led-sleeve.service /etc/systemd/system
echo "stopping led-sleeve..."
sudo systemctl stop led-sleeve
echo "reloading systemctl daemon..."
sudo systemctl daemon-reload
echo "setting led-sleeve to start on boot..."
sudo systemctl enable led-sleeve
echo "restarting led-sleeve..."
sudo systemctl start led-sleeve
