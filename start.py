from pi_wifi_bootstrap.pi_wifi_bootstrap import run_wifi_bootstrap
import asyncio

if __name__ == "__main__":
    asyncio.run(run_wifi_bootstrap(".", "sudo python3 -u led_sleeve.py"))
