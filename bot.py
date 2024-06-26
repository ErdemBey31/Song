import os, youtube_dl, requests, time
from config import Config
from youtube_search import YoutubeSearch
from pyrogram.handlers import MessageHandler
from pyrogram import Client, filters, idle
import yt_dlp
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)


#config#

bot = Client(
    'moonBot',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

#start mesajı

@bot.on_message(filters.command(['start']))
async def start_(client: Client, message: Message):
    await message.reply_sticker("CAACAgQAAxkBAAI8bmKIvgnlJyCrq9HIxSvCZCbm5CEjAAIaEAACpvFxHg-Z648-SCRWJAQ")
    await message.reply_text(
    f"""● **Selam** {message.from_user.mention}\n\n**» Ben müzik indirme botuyum istediğin müziği indirebilirim**\n\n**✅ Yardım için** /help **komutunu kullanın**\n\nVİDEOLU İNDİREBİLİRİM.""",
        reply_markup=InlineKeyboardMarkup(
            [[
                    InlineKeyboardButton('🇹🇷 𝖡𝖾𝗇𝗂 𝖦𝗋𝗎𝖻𝖺 𝖤𝗄𝗅𝖾 🇹🇷', url=f'http://t.me/muzikindirrobot?startgroup=new'),
                  ],[
                    InlineKeyboardButton('✅ 𝖣𝖾𝗌𝗍𝖾𝗄 ', url=f'https://t.me/eldembey'),
                    InlineKeyboardButton('⏳ 𝖪𝖺𝗇𝖺𝗅 ', url=f'https://t.me/eldembey')
                  ],[
                    InlineKeyboardButton('🧑🏻‍💻 ɢɪᴛʜᴜʙ ᴋᴀʏɴᴀᴋ ᴋᴏᴅᴜ 🧑🏻‍💻', url=f'https://nolur.com')
                ]
            ]
        )
    )
    
#yardım mesajı

@bot.on_message(filters.command(['help']))
def help(client, message):
    helptext = f'• **Müzik indirmek için /bul komutunu kullabilirsin .**\n\n**Örnek** :\n•> /bul `gece mavisi`\n/vbul <isim> videolu indir.'
    message.reply_text(
        text=helptext, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
            [[
                    InlineKeyboardButton('🇹🇷 𝖡𝖾𝗇𝗂 𝖦𝗋𝗎𝖻𝖺 𝖤𝗄𝗅𝖾 🇹🇷', url=f'http://t.me/muzikindirrobot?startgroup=new'),
                  ],[
                    InlineKeyboardButton('✅ 𝖣𝖾𝗌𝗍𝖾𝗄 ', url=f'https://t.me/eldembey'),
                    InlineKeyboardButton('⏳ 𝖪𝖺𝗇𝖺𝗅 ', url=f'https://t.me/eldembey')
                  ],[
                    InlineKeyboardButton('🧑🏻‍💻 ɢɪᴛʜᴜʙ ᴋᴀʏɴᴀᴋ ᴋᴏᴅᴜ 🧑🏻‍💻', url=f'https://nolur.com')
                ]
            ]
        )
    )
#alive mesaji#

@bot.on_message(filters.command("alive") & filters.user(Config.BOT_OWNER))
async def live(client: Client, message: Message):
    livemsg = await message.reply_text('`Merhaba Sahip 🌟`')
    
#musik indirme#

@bot.on_message(filters.command("bul") & ~filters.edited)
def bul(_, message):
    query = " ".join(message.command[1:])
    m = message.reply("<b>• **Şarkı Aranıyor** ...</b>")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        m.edit("<b>⛔ **Üzgünüm şarkı bulunamadı.**</b>")
        print(str(e))
        return
    m.edit("<b>•> **İndirme Başladı...**</b>")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"•>[ᴍᴘ3 ᴍᴜ̈ᴢɪᴋ ʙᴏᴛ](https://t.me/muzikindirrobot) 𝖳𝖺𝗋𝖺𝖿𝗂𝗇𝖽𝖺𝗇 !"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("•> **Yükleniyor**...")
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name, performer="ᴍᴘ3 ᴍᴜ̈ᴢɪᴋ ʙᴏᴛ")
        m.delete()
        bot.send_audio(chat_id=Config.PLAYLIST_ID, audio=audio_file, caption=rep, performer="ᴍᴘ3 ᴍᴜ̈ᴢɪᴋ ʙᴏᴛ", parse_mode='md', title=title, duration=dur, thumb=thumb_name)
    except Exception as e:
        m.edit(f"<b>⛔ Üzgünüm video bulunamadı.</b>\n\n<code> {e} </code>")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
@bot.on_message(filters.command("vbul") & ~filters.edited)
def bul(_, message):
    query = " ".join(message.command[1:])
    m = message.reply("<b>• **Video Aranıyor** ...</b>")
    ydl_ops = {"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        m.edit(f"<b>⛔ Üzgünüm video bulunamadı.</b>\n\n<code> {e} </code>")
        print(str(e))
        return
    m.edit("<b>•> **İndirme Başladı...**</b>")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            video_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"•>[ᴍᴘ4 ᴠɪᴅᴇᴏ ʙᴜ̈ᴛ](https://t.me/Muzikindirrobot) 𝖳𝖺𝗋𝖺𝖿𝗂𝗇𝖽𝖺𝗇 !"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("•> **Yükleniyor**...")
        message.reply_video(video_file, caption=rep, parse_mode='md', quote=False, title=title, duration=dur, thumb=thumb_name, performer="ᴍᴘ4 ᴠɪᴅᴇᴏ ʙᴜ̈ᴛ")
        m.delete()
        bot.send_video(chat_id=Config.PLAYLIST_ID, video=video_file, caption=rep, performer="ᴍᴘ4 ᴠɪᴅᴇᴏ ʙᴜ̈ᴛ", parse_mode='md', title=title, duration=dur, thumb=thumb_name)
    except Exception as e:
        m.edit(f"<b>⛔ Üzgünüm video bulunamadı.</b>\n\n<code> {e} </code>")
        print(e)

    try:
        os.remove(video_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
        
bot.start()
print(bot.get_me().username)
idle()
