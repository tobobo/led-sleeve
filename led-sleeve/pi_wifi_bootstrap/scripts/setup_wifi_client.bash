set -e

source "$(dirname "$0")/consts.bash"

sudo systemctl mask hostapd
sudo systemctl disable hostapd
sudo systemctl stop hostapd || echo "hostapd not running"

sudo systemctl disable dnsmasq
sudo systemctl stop dnsmasq || echo "dnsmasq not running"

sudo rfkill unblock wlan

sudo cp $DHCPCD_CONF_CLIENT_PATH $DHCPCD_CONF_PATH
sudo cp $DNSMASQ_CONF_CLIENT_PATH $DNSMASQ_CONF_PATH
if [ -f $HOSTAPD_CONF_PATH ]; then
  sudo rm $HOSTAPD_CONF_PATH
fi
if [ -f $IPTABLESV4_CONF_PATH ]; then
  sudo rm $IPTABLESV4_CONF_PATH
fi
if [ -f $IPTABLESV6_CONF_PATH ]; then
  sudo rm $IPTABLESV6_CONF_PATH
fi

echo "\
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
  ssid=\"$SSID\"
  psk=\"$PSK\"
}
" | sudo tee $WPASUPPLICANT_CONF_CLIENT_PATH

sudo cp $WPASUPPLICANT_CONF_CLIENT_PATH $WPASUPPLICANT_CONF_PATH

wpa_cli -i wlan0 reconfigure
