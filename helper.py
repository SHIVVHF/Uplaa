import subprocess
import datetime
import json
import asyncio
import os
import requests
import time
from p_bar import progress_bar
import gdown
import aiohttp
import tgcrypto
import aiofiles
from pyrogram.types import Message
from pyrogram import Client, filters
from subprocess import getstatusoutput

def duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

async def aio(url,name):
    k = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(k, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return k


async def download(url,name):
    ka = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(ka, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return ka

def vid_info(info):
    info = info.strip()
    info = info.split("\n")
    new_info = dict()
    temp = []
    for i in info:
        i = str(i)
        if "[" not in i and '---' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i.strip()
            i = i.split("|")[0].split(" ",3)
            try:
                if "RESOLUTION" not in i[2] and i[2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])

                    # temp.update(f'{i[2]}')
                    # new_info.append((i[2], i[0]))
                    #  mp4,mkv etc ==== f"({i[1]})"

                    new_info.update({f'{i[2]}':f'{i[0]}'})

            except:
                pass
    return new_info



async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if proc.returncode == 1:
        return False
    if stdout:
        return f'[stdout]\n{stdout.decode()}'
    if stderr:
        return f'[stderr]\n{stderr.decode()}'

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def time_name():
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return f"{date} {current_time}.mp4"

async def download_video(url,cmd, name):
    download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
    k = subprocess.run(download_cmd, shell=True)

    if "visionias" in cmd and k.returncode != 0:
        await asyncio.sleep(5)
        await download_video(url,cmd, name)
    try:
        if os.path.isfile(name):
            return name
        elif os.path.isfile(f"{name}.webm"):
            return f"{name}.webm"
        name = name.split(".")[0]
        if os.path.isfile(f"{name}.mkv"):
            return f"{name}.mkv"
        elif os.path.isfile(f"{name}.mp4"):
            return f"{name}.mp4"
        elif os.path.isfile(f"{name}.mp4.webm"):
            return f"{name}.mp4.webm"

        return name
    except FileNotFoundError as exc:
        return os.path.isfile.splitext[0] + "." + "mp4"

async def send_doc(bot: Client, m: Message,cc,ka,cc1,prog,count,name):
    reply = await bot.send_message(m.chat.id, f"Uploading - `{name}`")
    time.sleep(1)
    start_time = time.time()
    await bot.send.message(m.chat.id, ka,caption=cc1)
    count+=1
    await reply.delete (True)
    time.sleep(1)
    os.remove(ka)
    time.sleep(3)

async def send_vid(bot: Client, m: Message,cc,filename,thumb,name,prog):

    subprocess.run(f'ffmpeg -i "{filename}" -ss 00:00:12 -vframes 1 "{filename}.jpg"', shell=True)
    await prog.delete (True)
    reply = await bot.send_message(m.chat.id, f"**Uploading ...** - `{name}`")
    try:
        if thumb == "no":
            thumbnail = f"{filename}.jpg"
        else:
            thumbnail = thumb
    except Exception as e:
        await m.reply_text(str(e))

    dur = int(duration(filename))

    start_time = time.time()

    try:
        await bot.send_video(m.chat.id, filename,caption=cc, supports_streaming=True,height=480,width=640,thumb=thumbnail,duration=dur, progress=progress_bar,progress_args=(reply,start_time))
    except Exception:
        await bot.send_document(m.chat.id, filename,caption=cc, progress=progress_bar,progress_args=(reply,start_time))


    os.remove(filename)

    os.remove(f"{filename}.jpg")
    await reply.delete (True)

def get_video_attributes(file: str):
    """Returns video duration, width, height"""

    class FFprobeAttributesError(Exception):
        """Exception if ffmpeg fails to generate attributes"""

    cmd = (
        "ffprobe -v error -show_entries format=duration "
        + "-of default=noprint_wrappers=1:nokey=1 "
        + "-select_streams v:0 -show_entries stream=width,height "
        + f" -of default=nw=1:nk=1 '{file}'"
    )
    res, out = getstatusoutput(cmd)
    if res != 0:
        raise FFprobeAttributesError(out)
    width, height, dur = out.split("\n")
    return (int(float(dur)), int(width), int(height))