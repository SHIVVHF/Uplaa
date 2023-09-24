from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import json
import subprocess
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
import pyrogram
import tgcrypto
from p_bar import progress_bar
from details import api_id, api_hash, bot_token, sudo_group
from subprocess import getstatusoutput
import helper
import logging
import time
import glob
import aiohttp
import asyncio
import aiofiles
from pyrogram.types import User, Message
# import progressor
# from progressor import progress_for_pyrogram
import sys
import re
import os
import io
import pycurl

bot = Client(
     "bot",
      api_id=api_id,
      api_hash=api_hash,
      bot_token=bot_token)


@bot.on_message(filters.command("stop") & (filters.chat(sudo_group)))
async def restart_handler(_, m):
    await m.reply_text("𝖥𝗂𝗇𝖺𝗅𝗅𝗒 𝖱𝖾𝗌𝗍𝖺𝗋𝗍𝖾𝖽 😎!", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


def superSoup(link):
    req = requests.get(link, headers={'Referer': 'http://vod.visionias.in/'})
    if req.status_code != 200:
        return
    return BeautifulSoup(req.text, 'lxml')

def get_va(link):
    streamlink = superSoup(link)
    link = streamlink.find("script").string.split("url: ")[-1].split('",')[0].replace('"','')
    return link



@bot.on_message(filters.command(["txt"]) & (filters.chat(sudo_group)))
async def account_login(bot: Client, m: Message):
    editable = await bot.send_message(m.chat.id,
            " 𝖧𝖾𝗅𝗅𝗈 𝖡𝗋o🔥 How are u ?\n🔹 𝖨 𝖺𝗆 𝖳𝗑𝗍 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝖾𝗋 𝖡𝗈𝗍.\n🔹 𝖨 𝖼𝖺𝗇 𝖽𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝗏𝗂𝖽𝖾𝗈𝗌 𝖿𝗋𝗈𝗆 **𝗍𝗑𝗍** 𝖿𝗂𝗅𝖾 𝗈𝗇𝖾 𝖻𝗒 𝗈ne.\n🔹 Now Send Me the txt file and Wait.\n\n➠𝐌𝐨𝐝𝐢𝐟𝐢𝐞𝐝 𝐁𝐲: @ChVivekBro\n")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
        # print(len(links))
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    editable = await bot.send_message(m.chat.id,
        f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**"
    )
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text

    try:
        arg = int(raw_text) - 1
    except:
        arg = 1

    raw_text0 = input.document.file_name.replace(".txt", "").replace("_", " ")
    await input.delete(True)

    await bot.send_message(m.chat.id, "**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text

    editable = await bot.send_message(m.chat.id,
        "Now send the **Thumb url**\nEg : `https://te.legra.ph/file/e1fd929cee444772b18e8.jpg`\n\nor Send **no**"
    )
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if raw_text == '1':
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(arg, len(links)):

            url = links[i][1]
            name1 = links[i][0][:80].replace("\t", "").replace(":", "").replace("/","").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").strip()

            if "classplusapp" in url:
                headers = {
                    'Host': 'api.classplusapp.com',
                    'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6NTA5MTAzNjYsIm9yZ0lkIjo0MDU0NzMsInR5cGUiOjEsIm1vYmlsZSI6IjkxOTUyMDAzNjgzNCIsIm5hbWUiOiJSYW1wYWwiLCJlbWFpbCI6InNoYWxpbmlzaGFybWExNTA2OEBnbWFpbC5jb20iLCJpc0ludGVybmF0aW9uYWwiOjAsImRlZmF1bHRMYW5ndWFnZSI6IkVOIiwiY291bnRyeUNvZGUiOiJJTiIsImNvdW50cnlJU08iOiI5MSIsInRpbWV6b25lIjoiR01UKzU6MzAiLCJpc0RpeSI6ZmFsc2UsImZpbmdlcnByaW50SWQiOiI5MWU0MTYyODMxNjQxZGFjMTAzYWMyNGMzYjQxNTg4YyIsImlhdCI6MTY4MDI5NTY4MSwiZXhwIjoxNjgwOTAwNDgxfQ.q_iVpHJ1jgpHvb_v3b35AiyjrnW34PuWs00T5tWdyJn9Cm5tzI3ndKhY8I_sPmyn',
                    'user-agent': 'Mobile-Android',
                    'app-version': '1.4.37.1',
                    'api-version': '18',
                    'device-id': '5d0d17ac8b3c9f51',
                    'device-details':'2848b866799971ca_2848b8667a33216c_SDK-30',
                    'accept-encoding': 'gzip, deflate' }

                params = (('url', f'{url}'), )
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                url = response.json()['url']

            if '/master.mpd' in url:
             id =  url.split("/")[-2]
             url =  "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            if "visionias" in url:
                url = get_va(url)
                name = name1

            if raw_text2 == "144":

                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if '256x144' in out:
                    ytf = f"{out['256x144']}"
                elif '320x180' in out:
                    ytf = out['320x180']
                elif 'unknown' in out:
                    ytf = out["unknown"]
                else:
                    for data1 in out:
                        ytf = out[data1]
            elif raw_text2 == "180":

                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if '320x180' in out:
                    ytf = out['320x180']
                elif '426x240' in out:
                    ytf = out['426x240']
                elif 'unknown' in out:
                    ytf = out["unknown"]
                else:
                    for data2 in out:
                        ytf = out[data2]
            elif raw_text2 == "240":

                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if '426x240' in out:
                    ytf = out['426x240']
                elif '426x234' in out:
                    ytf = out['426x234']
                elif '480x270' in out:
                    ytf = out['480x270']
                elif '480x272' in out:
                    ytf = out['480x272']
                elif '640x360' in out:
                    ytf = out['640x360']
                elif 'unknown' in out:
                    ytf = out["unknown"]
                else:
                    for data3 in out:
                        ytf = out[data3]
            elif raw_text2 == "360":

                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if '640x360' in out:
                    ytf = out['640x360']
                elif '638x360' in out:
                    ytf = out['638x360']
                elif '636x360' in out:
                    ytf = out['636x360']
                elif '768x432' in out:
                    ytf = out['768x432']
                elif '638x358' in out:
                    ytf = out['638x358']
                elif '852x316' in out:
                    ytf = out['852x316']
                elif '850x480' in out:
                    ytf = out['850x480']
                elif '848x480' in out:
                    ytf = out['848x480']
                elif '854x480' in out:
                    ytf = out['854x480']
                elif '852x480' in out:
                    ytf = out['852x480']
                elif '854x470' in out:
                    ytf = out['852x470']
                elif '1280x720' in out:
                    ytf = out['1280x720']
                elif 'unknown' in out:
                    ytf = out["unknown"]
                else:
                    for data4 in out:
                        ytf = out[data4]
            elif raw_text2 == "480":

                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if '854x480' in out:
                    ytf = out['854x480']
                elif '852x480' in out:
                    ytf = out['852x480']
                elif '854x470' in out:
                    ytf = out['854x470']
                elif '768x432' in out:
                    ytf = out['768x432']
                elif '848x480' in out:
                    ytf = out['848x480']
                elif '850x480' in out:
                    ytf = out['850x480']
                elif '960x540' in out:
                    ytf = out['960x540']
                elif '640x360' in out:
                    ytf = out['640x360']
                elif 'unknown' in out:
                    ytf = out["unknown"]
                else:
                    for data5 in out:
                        ytf = out[data5]

            elif raw_text2 == "720":

                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if '1280x720' in out:
                    ytf = out['1280x720']
                elif '1280x704' in out:
                    ytf = out['1280x704']
                elif '1280x474' in out:
                    ytf = out['1280x474']
                elif '1920x712' in out:
                    ytf = out['1920x712']
                elif '1920x1056' in out:
                    ytf = out['1920x1056']
                elif '854x480' in out:
                    ytf = out['854x480']
                elif '640x360' in out:
                    ytf = out['640x360']
                elif 'unknown' in out:
                    ytf = out["unknown"]
                else:
                    for data6 in out:
                        ytf = out[data6]
            elif "player.vimeo" in url:
                if raw_text2 == '144':
                    ytf = 'http-240p'
                elif raw_text2 == "240":
                    ytf = 'http-240p'
                elif raw_text2 == '360':
                    ytf = 'http-360p'
                elif raw_text2 == '480':
                    ytf = 'http-540p'
                elif raw_text2 == '720':
                    ytf = 'http-720p'
                else:
                    ytf = 'http-360p'
            else:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                for dataS in out:
                    ytf = out[dataS]


            try:
                if "unknown" in out:
                    res = "NA"
                else:
                    res = list(out.keys())[list(out.values()).index(ytf)]

                name = f'{str(count).zfill(3)}) {name1} {res}'
            except Exception:
                res = "NA"

            # if "youtu" in url:
            # if ytf == f"'bestvideo[height<={raw_text2}][ext=mp4]+bestaudio[ext=m4a]'" or "acecwply" in url:
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'
            # print
            try:
                Show = f"**Downloading** :-\n**Name :-** `{name}\nQuality - {raw_text2}`\n\n**Bot By:** ChVivekBro 🇮🇳"
                prog = await bot.send_message(m.chat.id, Show)
                cc = f"{str(count).zfill(3)}. {name1} {res}🇻 🇮 🇻 🇪 🇰.mp4\n\n**Batch :** {raw_text0}\n**Quality :** {raw_text2}\n\n**Extracted By ➤** 𝐕𝐢𝐯𝐞𝐤 𝐓𝐨𝐦𝐚𝐫™ 🇮🇳"
                cc1 = f"{str(count).zfill(3)}. {name1}🇻 🇮 🇻 🇪 🇰.pdf\n\n**Batch :** {raw_text0}\n**Quality :** {raw_text2}\n\n**Extracted By ➤** 𝐕𝐢𝐯𝐞𝐤 𝐓𝐨𝐦𝐚𝐫™ 🇮🇳"

                if cmd == "pdf" in url or ".pdf" in url or ".pdf" in name1 or "drive" in url:
                    try:
                        ka = await helper.aio(url, name)
                        await prog.delete(True)
                        reply = await bot.send_message(m.chat.id, f"Uploading - ```{name}```")
                        time.sleep(1)
                        start_time = time.time()
                        await bot.send_document(m.chat.id, ka, caption=cc1)
                        count += 1
                        # time.sleep(2)
                        await reply.delete(True)
                        time.sleep(1)
                        os.remove(ka)
                        time.sleep(4)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await helper.send_vid(bot, m, cc, filename, thumb, name,
                                          prog)
                    count += 1
                    time.sleep(3)

            except Exception as e:
                await m.reply_text(
                    f"**downloading failed ❌**\n{str(e)}\n**Name** - {name}\n**Link** - `{url}`"
                )
                count += 1
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("Done")


bot.run()
