import sys
import os
thisdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(thisdir)

import asyncio
import logging
from wifi_setup_server import get_credentials_from_server
from stream_command import stream_command

logging.basicConfig(level=logging.DEBUG)


async def stream_with_labeled_output(label, cmd, env={}):
    return await stream_command(
        cmd,
        lambda x: logging.debug(f"{label}: {x.decode()[:-1]}"),
        lambda x: logging.debug(f"{label}_stderr: {x.decode()[:-1]}"),
        env
    )


async def is_command_successful(cmd, label, env={}):
    proc = await stream_with_labeled_output(cmd, label, env)
    return proc.returncode == 0


async def is_ap():
    logging.info("main: checking if ap")
    return await is_command_successful("is_ap", ["systemctl", "status", "hostapd"])


async def has_wifi_connection():
    logging.info("main: checking wifi connection")
    return await is_command_successful("check_wifi", ["bash", f"{thisdir}/scripts/check_wifi_connection.bash"])


async def set_credentials(ssid, psk):
    await stream_with_labeled_output("set_credentials", ["bash", f"{thisdir}/scripts/setup_wifi_client.bash"], {'SSID': ssid, 'PSK': psk})


async def enable_ap():
    logging.info("main: enabling ap")
    await stream_with_labeled_output("enable_ap", ["bash", f"{thisdir}/scripts/setup_wifi_ap.bash"])


async def run_wifi_bootstrap(app_directory, app_command):
    while True:
        if await is_ap():
            logging.info(
                "main: access point enabled, get credentials from wifi setup app")
            ssid, psk = await get_credentials_from_server()
            await set_credentials(ssid, psk)
        elif await has_wifi_connection():
            logging.info("main: has wifi connection, run app server")
            await stream_with_labeled_output(
                "app",
                ["bash", "-c", f"cd {app_directory} && {app_command}"]
            )
        else:
            logging.info("main: no connection, enable ap")
            await enable_ap()


if __name__ == "__main__":
    asyncio.run(run_wifi_bootstrap(".", "python3 -u test_app.py"))
