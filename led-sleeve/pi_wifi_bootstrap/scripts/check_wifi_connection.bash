set -e

source "$(dirname "$0")/consts.bash"

if sudo cat /etc/wpa_supplicant/wpa_supplicant.conf | grep ssid; then
  for ((n=1;n<=15;n++)); do
    { iwgetid && echo "Connected to wifi" && exit 0; } \
      || echo "Failed wifi check $n times" && sleep 2
  done
  echo "Not connected to wifi"
  exit 1
else
  echo "Initial setup"
  exit 1
fi
