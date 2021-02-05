set -e

source "$(dirname "$0")/consts.bash"

sudo cp $DHCPCD_CONF_AP_PATH $DHCPCD_CONF_PATH
sudo cp $DNSMASQ_CONF_AP_PATH $DNSMASQ_CONF_PATH
sudo cp $HOSTAPD_CONF_AP_PATH $HOSTAPD_CONF_PATH
sudo cp $WPASUPPLICANT_CONF_AP_PATH $WPASUPPLICANT_CONF_PATH
sudo cp $IPTABLESV4_CONF_AP_PATH $IPTABLESV4_CONF_PATH
sudo cp $IPTABLESV6_CONF_AP_PATH $IPTABLESV6_CONF_PATH

wpa_cli -i wlan0 reconfigure

sudo systemctl unmask hostapd
sudo systemctl enable hostapd

sudo systemctl enable dnsmasq

sudo rfkill unblock wlan

sudo systemctl start hostapd
sudo systemctl start dnsmasq
