import asyncio
from pi_wifi_bootstrap.pi_wifi_bootstrap import run_wifi_bootstrap

if __name__ == "__main__":
    asyncio.run(run_wifi_bootstrap(".", "sudo python3 -u led_sleeve.py"))
