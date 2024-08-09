from FZBypass import Bypass, LOGGER, Config
from pyrogram import idle
from pyrogram.filters import command, user
from os import path as ospath, execl
from asyncio import create_subprocess_exec
from sys import executable
import asyncio
import aiohttp
import traceback
logging = LOGGER

@Bypass.on_message(command('restart') & user(Config.OWNER_ID))
async def restart(client, message):
    restart_message = await message.reply('<i>Restarting...</i>')
    await (await create_subprocess_exec('python3', 'update.py')).wait()
    with open(".restartmsg", "w") as f:
        f.write(f"{restart_message.chat.id}\n{restart_message.id}\n")
    execl(executable, executable, "-m", "FZBypass")

async def restart():
    if ospath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        try:
            await Bypass.edit_message_text(chat_id=chat_id, message_id=msg_id, text="<i>Restarted !</i>")
        except Exception as e:
            LOGGER.error(e)
    asyncio.create_task(ping_server())

async def ping_server():
    sleep_time = 40#300
    url = "https://hkmirzamim.onrender.com"
    while True:
        await asyncio.sleep(sleep_time)
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get(url) as resp:
                    print(resp.status)
                    #logging.info("Pinged server with response: {}".format(resp.status))
        except TimeoutError:
            logging.warning("Couldn't connect to the site URL..!")
        except Exception:
            traceback.print_exc()

Bypass.start()
LOGGER.info('FZ Bot Started!')
Bypass.loop.run_until_complete(restart())
idle()
Bypass.stop()
