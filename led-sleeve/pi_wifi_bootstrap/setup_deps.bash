set -e

source "$(dirname "$0")/scripts/consts.bash"

which hostapd || sudo apt-get install -y hostapd || { echo "Installing hostapd failed"; exit 1; }

which dnsmasq || sudo apt-get install -y dnsmasq || { echo "Installing dnsmasq failed"; exit 1; }

which netfilter-persistent || sudo DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent || { echo "Installing netfilter-persistent failed"; exit 1; }
which iptables-persistent || sudo DEBIAN_FRONTEND=noninteractive apt install -y iptables-persistent || { echo "Installing iptables-persistent failed"; exit 1; }

sudo cp $DHCPCD_CONF_PATH $DHCPCD_CONF_ORIG_PATH
sudo cp $DHCPCD_CONF_PATH $DHCPCD_CONF_AP_PATH
sudo cp $DHCPCD_CONF_PATH $DHCPCD_CONF_CLIENT_PATH

sudo echo "
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
" | sudo tee -a $DHCPCD_CONF_AP_PATH

sudo cp $DNSMASQ_CONF_PATH $DNSMASQ_CONF_ORIG_PATH
sudo cp $DNSMASQ_CONF_PATH $DNSMASQ_CONF_AP_PATH
sudo cp $DNSMASQ_CONF_PATH $DNSMASQ_CONF_CLIENT_PATH

sudo echo "
interface=wlan0 # Listening interface
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
                # Pool of IP addresses served via DHCP
domain=wlan     # Local wireless DNS domain
address=/gw.wlan/192.168.4.1
                # Alias for this router
" | sudo tee -a $DNSMASQ_CONF_AP_PATH

sudo echo "
country_code=US
interface=wlan0
ssid=rpi-testnetwork
hw_mode=g
channel=7
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=testpass
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
" | sudo tee -a $HOSTAPD_CONF_AP_PATH

sudo cp $IPTABLESV4_CONF_PATH $IPTABLESV4_CONF_AP_PATH
sudo cp $IPTABLESV6_CONF_PATH $IPTABLESV6_CONF_AP_PATH

sudo cp $WPASUPPLICANT_CONF_PATH $WPASUPPLICANT_CONF_ORIG_PATH
sudo cp $WPASUPPLICANT_CONF_PATH $WPASUPPLICANT_CONF_AP_PATH
sudo cp $WPASUPPLICANT_CONF_PATH $WPASUPPLICANT_CONF_CLIENT_PATH

sudo apt-get install -y python3-pip
sudo python3 -m pip install -r requirements.txt
