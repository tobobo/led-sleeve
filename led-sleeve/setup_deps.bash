set -e

THIS_DIR=$(dirname "$0")
# Set up wifi bootstrap
bash "$THIS_DIR/pi_wifi_bootstrap/setup_deps.bash"

sudo apt-get update

# Set up rgb led matrix scripts
reconfig() {
	grep $2 $1 >/dev/null
	if [ $? -eq 0 ]; then
		# Pattern found; replace in file
		sed -i "s/$2/$3/g" $1 >/dev/null
	else
		# Not found; append (silently)
		echo $3 | sudo tee -a $1 >/dev/null
	fi
}

pushd "$THIS_DIR/lib/rpi-rgb-led-matrix/bindings/python"
make build-python
sudo make install-python
popd
reconfig /boot/config.txt "^.*dtparam=audio.*$" "dtparam=audio=off"

# Install other dependencies
sudo apt-get install -y imagemagick

# Install python requirements
sudo python3 -m pip install -r "$THIS_DIR/requirements.txt"
