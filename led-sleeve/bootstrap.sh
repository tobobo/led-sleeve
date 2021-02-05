SERVICE_FILE_NAME=led-sleeve.service
LOCAL_SERVICE_FILE=$(dirname "$0")/$SERVICE_FILE_NAME
SYSTEM_SERVICE_DIR=/etc/systemd/system
SYSTEM_SERVICE_FILE=$SYSTEM_SERVICE_DIR/$SERVICE_FILE_NAME

echo "stopping led-sleeve..."
sudo systemctl stop led-sleeve
if ! cmp -s "$LOCAL_SERVICE_FILE" "$SYSTEM_SERVICE_FILE"; then
  sudo cp -v $LOCAL_SERVICE_FILE $SYSTEM_SERVICE_DIR
  echo "reloading systemctl daemon..."
  sudo systemctl daemon-reload
  echo "setting led-sleeve to start on boot..."
  sudo systemctl enable led-sleeve
fi
echo "restarting led-sleeve..."
sudo systemctl start led-sleeve
