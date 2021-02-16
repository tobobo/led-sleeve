import os
import asyncio
import logging


async def _read_stream(stream, line_cb):
    while True:
        line = await stream.readline()
        if line:
            line_cb(line)
        else:
            break


async def stream_command_raw(cmd, stdout_cb, stderr_cb, env):
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE,
        env=dict(os.environ, **env)
    )

    stdout_task = asyncio.create_task(_read_stream(process.stdout, stdout_cb))
    stderr_task = asyncio.create_task(_read_stream(process.stderr, stderr_cb))

    return process, stdout_task, stderr_task


async def stream_command(cmd, stdout_cb, stderr_cb, env):
    process, stdout_task, stderr_task = await stream_command_raw(cmd, stdout_cb, stderr_cb, env)

    await asyncio.gather(stdout_task, stderr_task)
    await process.wait()

    return process


async def stream_with_labeled_output(label, cmd, env=None):
    if env is None:
        env = {}
    return await stream_command(
        cmd,
        lambda x: logging.debug(f"{label}: {x.decode()[:-1]}"),
        lambda x: logging.debug(f"{label}_stderr: {x.decode()[:-1]}"),
        env
    )


async def stream_with_labeled_output_raw(label, cmd, env=None):
    if env is None:
        env = {}
    return await stream_command_raw(
        cmd,
        lambda x: logging.debug(f"{label}: {x.decode()[:-1]}"),
        lambda x: logging.debug(f"{label}_stderr: {x.decode()[:-1]}"),
        env
    )

async def get_stdout(cmd, env=None):
    if env is None:
        env = {}

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env
    )
    
    stdout, stderr = await proc.communicate()
    if stdout:
        return stdout.decode()
    else:
        return None
