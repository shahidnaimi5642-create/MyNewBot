import os
import threading
import json
import time
import telebot
from telebot import types

# مشخصات اصلی ربات شما
BOT_TOKEN = "8844218622:AAHeSyvfy31XjtJ-pGf5_r9vjrUUsOR44n4"
ADMIN_ID = 8173349543
DB_FILE = "users_database4.json"

bot_items = {
    # --- بخش برنامه‌ها ---
    "1": {"name": {"fa": "برنامه هک فیسبوک 👤", "ps": "د فېسبوک هک کولو برنامه 👤", "en": "Facebook Hack App 👤"}, "type": "file", "file_id": "BQACAgUAAxkBAAMzah8llfBmnrkBU1yph3X6kqfHBrEAAuceAALeRfhU5SKcVKyFmX87BA", "points": 25, "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"},
    "2": {"name": {"fa": "برنامه هک گالری 📱", "ps": "د ګالري هک کولو برنامه 📱", "en": "Gallery Hack App 📱"}, "type": "file", "file_id": "BQACAgUAAxkBAAMmah8kDxmksVQJG6iHFIkw4_dhkCEAAuAeAALeRfhUeDI4vKQI7pU7BA", "points": 20, "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"},
    "3": {"name": {"fa": "برنامه هک تمام گوشی 💻", "ps": "د ټول موبایل هک کولو برنامه 💻", "en": "Full Phone Hack App 💻"}, "type": "file", "file_id": "BQACAgUAAxkBAAM2ah8lw6eUoD7DLMJrtV01tSTP_dAAAugeAALeRfhUyClX4GTPAc47BA", "points": 40, "caption": " 👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"},
    "4": {"name": {"fa": "برنامه فارمت گالری ⚠️", "ps": "د ګالري فارمټ کولو برنامه ⚠️", "en": "Gallery Format App ⚠️"}, "type": "file", "file_id": "BQACAgUAAxkBAAM4ah8mSF6bEz-BTdEKt1FxFKkFR2QAAukeAALeRfhUGLM7vW_QFbs7BA", "points": 30, "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"},
    "5": {"name": {"fa": "برنامه هک پیامک 💬", "ps": "د اس‌ام‌اس هک کولو برنامه 💬", "en": "SMS Hack App 💬"}, "type": "file", "file_id": "BQACAgUAAxkBAAMwah8lkiwXb7h-KtUDdq_JJonmIZwAAuUeAALeRfhUs-bTgryrn8o7BA", "points": 25, "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"},
    "6": {"name": {"fa": "برنامه هک مخاطبین 📞", "ps": "د مخاطبینو هک کولو برنامه 📞", "en": "Contacts Hack App 📞"}, "type": "file", "file_id": "BQACAgUAAxkBAAMyah8llWQWGuh1eMMoD9T7OfrATD4AAuYeAALeRfhUP6utrnLpNMI7BA", "points": 20, "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"},
    "7": {"name": {"fa": "برنامه هک تلگرام ✈️", "ps": "د ټیلیګرام هک کولو برنامه ✈️", "en": "Telegram Hack App ✈️"}, "type": "file", "file_id": "BQACAgUAAxkBAAMqah8lMmvh3q_2BbjR4EtZC7E6NYkAAuIeAALeRfhUFpxV7WLf6ZQ7BA", "points": 35, "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"},
    "8": {"name": {"fa": "برنامه هک واستاپ 🟢", "ps": "د واټساپ هک کولو برنامه 🟢", "en": "WhatsApp Hack App 🟢"}, "type": "file", "file_id": "BQACAgUAAxkBAAMoah8k8grrGuHPUIqM63NrB8-C_MQAAuEeAALeRfhUYcfFr96wl3A7BA", "points": 35, "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"},
    "9": {"name": {"fa": "برنامه متن‌های بند و رفع بند 📝", "ps": "د بند او رفع بند متنونو برنامه 📝", "en": "Ban & Unban Texts App 📝"}, "type": "file", "file_id": "BQACAgUAAxkBAAMsah8lPWS5L_E4YlI7c8YOTfs8uaIAAuMeAALeRfhUPBbKxAn_Ifs7BA", "points": 20, "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"},
    "10": {"name": {"fa": "برنامه ایدت برنامه 🛠️", "ps": "د اپلیکیشن ایډیټ کولو برنامه 🛠️", "en": "App Editing Tool 🛠️"}, "type": "file", "file_id": "BQACAgUAAxkBAAMuah8ljbBPdmm1iapt7IPIvyQqtG4AAuQeAALeRfhU7BCdDXzNImw7BA", "points": 30, "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"},
    "11": {"name": {"fa": "برنامه قفل موبایل 🔒", "ps": "د موبایل لاک کولو برنامه 🔒", "en": "Phone Locker App 🔒"}, "type": "file", "file_id": "BQACAgAIBvGogaVVIUK403_LwrBPR50f_Nv-tAAKjIAAC4o4BVe6MWfTtch-pOwQ", "points": 30, "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"},
    "18": {
        "name": {"fa": "برنامه پوشه نامحدود 📁", "ps": "د نامحدوده فولډرونو برنامه 📁", "en": "Unlimited Folders App 📁"}, "type": "file",
        "file_id": "BQACAgIAAxkBAAIE0GpGcvb5TKiFCN2LLCns_sEj5iSCAAI4FwACVUUISMEho_IZQCb-PAQ",
        "points": 25, "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"
    },
    "19": {
        "name": {"fa": "برنامه خاموش شدن موبایل 💤", "ps": "د موبایل مړه کولو برنامه 💤", "en": "Phone Shutdown App 💤"}, "type": "file",
        "file_id": "BQACAgIAAxkBAAIE1WpGc5JcFoqfa-AgtTWZ10QwHDwLAAL2EgACk92pS__iCfq0AsspPAQ",
        "points": 30, "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"
    },
    "20": {
        "name": {"fa": "ویروس سخت اندروید 💀", "ps": "سخت اندروید ویروس 💀", "en": "Hard Android Virus 💀"}, "type": "file",
        "file_id": "BQACAgIAAxkBAAIE12pGdA-fQ7mXlG78DLuXY-ayORGbAAKkFAACvY7JS7kd_uMl9jfsPAQ",
        "points": 35, "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"
    },
    "21": {
        "name": {"fa": "ویروس فرمت کامل گوشی 🔄", "ps": "د موبایل بشپړ فارمټ ویروس 🔄", "en": "Full Phone Format Virus 🔄"}, "type": "file",
        "file_id": "BQACAgQAAxkBAAIE3mpGdOAOWwb86GAWr9jr8dSGX-xyAAK4CwACSxdJU64UWhKnNQgPPAQ",
        "points": 40, "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"
    },
    "22": {
        "name": {"fa": "ویروس واتساپ ☣️", "ps": "د واټساپ ویروس ☣️", "en": "WhatsApp Virus ☣️"}, "type": "file",
        "file_id": "BQACAgQAAxkBAAIE4GpGdXDHqAM6cTgps4lvMmoRNojEAAJAEAACwEYIUdic9BGhwdE2PAQ", "points": 35,
        "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"
    },
    "37": {
        "name": {"fa": "برنامه واتساپ عربی ویژه 🇸🇦", "ps": "د ځانګړي عربي واټساپ برنامه 🇸🇦", "en": "Special Arabic WhatsApp App 🇸🇦"}, "type": "file",
        "file_id": "BQACAgQAAxkBAAIGHmpLTZMotG7mMMR3fBgvfljiIZYGAAK5HAACLUCAUe7RPiyWaXjpPAQ",
        "points": 200, "caption": "👤 ساخته شده توسط رئیس شاهد | د رئیس شاهد لخوا جوړ شوی | Created by Raees Shahid"
    },
    # --- بخش ربات‌ها و سایت‌ها ---
    "12": {"name": {"fa": "سایت شماره افغانی 🌐", "ps": "د افغاني شمېرو سایټ 🌐", "en": "Afghan Number Site 🌐"}, "type": "link", "username": "@msnumber2_bot", "points": 20},
    "13": {"name": {"fa": "سایت شماره جرمنی 🌐", "ps": "د جرمني شمېرو سایټ 🌐", "en": "Germany Number Site 🌐"}, "type": "link", "username": "@NumberNest_2_Bot", "points": 25},
    "14": {"name": {"fa": "سایت شماره فرانسه 🌐", "ps": "د فرانسې شمېرو سایټ 🌐", "en": "France Number Site 🌐"}, "type": "link", "username": "@Unlimited_Numbers1_bot", "points": 25},
    "15": {"name": {"fa": "سایت شماره یمن 🌐", "ps": "د یمن شمېرو سایټ 🌐", "en": "Yemen Number Site 🌐"}, "type": "link", "username": "@AllNumbersStoreBot", "points": 20},
    "16": {"name": {"fa": "ربات هک کامره 🤖", "ps": "د کامرې هک کولو بوټ 🤖", "en": "Camera Hack Bot 🤖"}, "type": "link", "username": "@Cameravipbot", "points": 30},
    "17": {"name": {"fa": "هک لوکیشن و کامره جدید 🤖", "ps": "د لوکیشن او کامرې نوی هک 🤖", "en": "New Location & Camera Hack 🤖"}, "type": "link", "username": "@Kali_Linux_Robot", "points": 35},
    "23": {"name": {"fa": "ربات هک تمام رسانه اجتماعی 🌐", "ps": "د ټولو ټولنیزو رسنیو هک کولو بوټ 🌐", "en": "All Social Media Hack Bot 🌐"}, "type": "link", "username": "@qii7cbot", "points": 300},
    "24": {"name": {"fa": "ربات جیمیل‌های فیک ✉️", "ps": "د جعلي جیمیلونو بوټ ✉️", "en": "Fake Gmail Bot ✉️"}, "type": "link", "username": "@MailNoxBot", "points": 20},
    "25": {"name": {"fa": "ربات دریافت آیدی عددی 🆔", "ps": "د عددي آیدي ترلاسه کولو بوټ 🆔", "en": "Get Numerical ID Bot 🆔"}, "type": "link", "username": "@userinfofastbot", "points": 15},
    "26": {"name": {"fa": "ربات هوش مصنوعی ساخت آهنگ 🎵", "ps": "د سندرو جوړولو په کچه ځیرکتیا بوټ 🎵", "en": "AI Music Generator Bot 🎵"}, "type": "link", "username": "@jggl_ai_bot", "points": 30},
    "27": {"name": {"fa": "ربات ویروس واتساپ ☣️", "ps": "د واټساپ ویروس بوټ ☣️", "en": "WhatsApp Virus Bot ☣️"}, "type": "link", "username": "@holowxsbot", "points": 40},
    "28": {"name": {"fa": "ربات دانلود آهنگ از همه‌جا 🎧", "ps": "د سندرو ډاونلوډ کولو بوټ 🎧", "en": "Music Downloader Bot 🎧"}, "type": "link", "username": "@whatsmusicbot", "points": 15},
    "29": {"name": {"fa": "ربات دانلود از تیک‌تاک 🎬", "ps": "د ټیک ټاک ډاونلوډ کولو بوټ 🎬", "en": "TikTok Downloader Bot 🎬"}, "type": "link", "username": "@TiktokFiler_Bot", "points": 15},
    "30": {"name": {"fa": "ربات افزایش کیفیت عکس 📸", "ps": "د عکس کیفیت لوړولو بوټ 📸", "en": "Photo Quality Enhancer Bot 📸"}, "type": "link", "username": "@PhotoAi_robot", "points": 20},
    "31": {"name": {"fa": "ربات هوش مصنوعی تبدیل متن به عکس 🎨", "ps": "له متن څخه د عکس جوړولو بوټ 🎨", "en": "Text to Image AI Bot 🎨"}, "type": "link", "username": "@SomniumBot", "points": 25},
    "32": {"name": {"fa": "ربات تبدیل عکس به انیمه 👑", "ps": "د عکس انیمه کولو بوټ 👑", "en": "Photo to Anime Bot 👑"}, "type": "link", "username": "@AnimeLabBot", "points": 25},
    "33": {"name": {"fa": "ربات زیباساز و فونت‌ساز 📝", "ps": "د فونټونو او ښکلا جوړولو بوټ 📝", "en": "Font Stylist Bot 📝"}, "type": "link", "username": "@fontesmirbot", "points": 15},
    "34": {"name": {"fa": "ربات لخت کردن عکس (هوش مصنوعی) 🔞", "ps": "د عکسونو بربنډولو بوټ 🔞", "en": "Nude AI Photo Bot 🔞"}, "type": "link", "username": "@PhotoStudioXBot", "points": 50},
    "35": {"name": {"fa": "ربات دانلود از اینستاگرام 📥", "ps": "د انسټاګرام ډاونلوډ کولو بوټ 📥", "en": "Instagram Downloader Bot 📥"}, "type": "link", "username": "@instasavejnbot", "points": 15},
    "36": {"name": {"fa": "ربات دانلود از یوتیوب 🎥", "ps": "د یوټیوب ډاونلوډ کولو بوټ 🎥", "en": "YouTube Downloader Bot 🎥"}, "type": "link", "username": "@YouTubedl_dl_bot", "points": 20},
    "38": {"name": {"fa": "ربات هک تمام اطلاعات گوشی 📱", "ps": "د موبایل د ټولو معلوماتو هک کولو بوټ 📱", "en": "Full Phone Info Hack Bot 📱"}, "type": "link", "username": "@hackfreeusrbot", "points": 250}
}

# متون چندزبانه سیستم
LANG_TEXTS = {
    "select_lang": "Please choose your language / مهرباني وکړئ خپله ژبه غوره کړئ / لطفاً زبان خود را انتخاب کنید:",
    "welcome": {
        "fa": "سلام! به ربات بزرگ ابزارهای هک و شماره مجازی خوش آمدید. از منوی زیر استفاده کنید:",
        "ps": "سلام! د هک وسیلو او مجازي شمیرو لوی بوټ ته ښه راغلاست. له لاندې مینو څخه ګټه پورته کړئ:",
        "en": "Hello! Welcome to the Great Hacking Tools & Virtual Numbers Bot. Use the menu below:"
    },
    "btn_apps": {"fa": "📥 دانلود برنامه‌های هک", "ps": "📥 د هک پروګرامونو ډاونلوډ", "en": "📥 Download Hack Apps"},
    "btn_links": {"fa": "🔗 ربات‌ها و سایت‌های مجازی", "ps": "🔗 مجازي بوټان او سایټونه", "en": "🔗 Virtual Bots & Sites"},
    "btn_daily": {"fa": "🎁 سکه روزانه", "ps": "🎁 ورځنۍ سکه", "en": "🎁 Daily Bonus"},
    "btn_support": {"fa": "📞 پشتیبانی", "ps": "📞 ملاتړ (پشتیواني)", "en": "📞 Support"},
    "btn_myinfo": {"fa": "👤 اطلاعات من / لینک دعوت", "ps": "👤 زما معلومات / د بلنې لینک", "en": "👤 My Info / Invite Link"},
    "btn_buy": {"fa": "💳 خرید امتیاز", "ps": "💳 د امتیازانو پېرل", "en": "💳 Buy Points"},
    "btn_changelang": {"fa": "🌐 تغییر زبان / ژبه بدلول / Change Language", "ps": "🌐 تغییر زبان / ژبه بدلول / Change Language", "en": "🌐 تغییر زبان / ژبه بدلول / Change Language"},
    "daily_success": {
        "fa": "🎁 تبریک! تعداد 2 امتیاز روزانه به شما تعلق گرفت.\n\n👤 ساخته شده توسط رئیس شاهد",
        "ps": "🎁 مبارک شه! تاسو ته ۲ ورځني امتیازونه درکړل شول.\n\n👤 د رئیس شاهد لخوا جوړ شوی",
        "en": "🎁 Congratulations! You received 2 daily points.\n\n👤 Created by Raees Shahid"
    },
    "daily_fail": {
        "fa": "❌ شما امروز هدیه خود را دریافت کرده‌اید!\n\n👤 ساخته شده توسط رئیس شاهد",
        "ps": "❌ تاسو نن خپله ډالۍ ترلاسه کړې ده!\n\n👤 د رئیس شاهد لخوا جوړ شوی",
        "en": "❌ You have already claimed your bonus today!\n\n👤 Created by Raees Shahid"
    },
    "insufficient_points": {
        "fa": "❌ امتیاز شما کافی نیست!", "ps": "❌ ستاسو امتیازونه کافي ندي!",
        "en": "❌ Insufficient points!"
    },
    "ask_buy": {
        "fa": "⚠️ آیا مطمئن هستید که می‌خواهید محصول **{}** را در ازای **{} امتیاز** دریافت کنید؟",
        "ps": "⚠️ ایا ډاډه یاست چې غواړئ **{}** محصول د **{} امتیازونو** په بدل کې ترلاسه کړئ؟",
        "en": "⚠️ Are you sure you want to get **{}** for **{} points**?"
    },
    "security_warn": {
        "fa": "\n\n⚠️ هشدار امنیت: این پیام به دلیل حفظ امنیت بعد از ۳۰ ثانیه خودکار حذف خواهد شد!",
        "ps": "\n\n⚠️ د امنیت خبرتیا: دا پیغام به د امنیت ساتلو لپاره وروسته له ۳۰ ثانیو په اتوماتیک ډول حذف شي!",
        "en": "\n\n⚠️ Security Warning: This message will be auto-deleted after 30 seconds for security reasons!"
    },
    "support_msg": {
        "fa": "✍️ لطفا پیام خود را بنویسید:\n\nربات پیام شما را مستقیم به دست رئیس شاهد می‌رساند.",
        "ps": "✍️ مهرباني وکړئ خپل پیغام ولیکئ:\n\nبوټ ستاسو پیغام مستقیم رئیس شاهد ته رسوي.",
        "en": "✍️ Please write your message:\n\nThe bot will deliver it directly to Raees Shahid."
    },
    "support_success": {
        "fa": "✅ پیام شما مستقیماً برای رئیس شاهد ارسال شد.",
        "ps": "✅ ستاسو پیغام په مستقیم ډول رئیس شاهد ته واستول شو.",
        "en": "✅ Your message has been successfully sent to Raees Shahid."
    }
}

bot = telebot.TeleBot(BOT_TOKEN)
users_db = {}
user_state = {}
BOT_STATUS_FILE = "bot_status.json"
bot_status = {"active": True}

if os.path.exists(BOT_STATUS_FILE):
    with open(BOT_STATUS_FILE, "r") as f:
        try: bot_status = json.load(f)
        except: bot_status = {"active": True}

def save_status():
    with open(BOT_STATUS_FILE, "w") as f: json.dump(bot_status, f)

if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        try: users_db = json.load(f)
        except: users_db = {}

def save_db():
    with open(DB_FILE, "w") as f: json.dump(users_db, f, indent=4)

def get_user_data(user_id):
    uid = str(user_id)
    if uid not in users_db:
        users_db[uid] = {"points": 0, "referred_by": None, "last_daily": None, "status": "normal", "referrals_count": 0, "lang": None}
        save_db()
    if "lang" not in users_db[uid]:
        users_db[uid]["lang"] = None
    return users_db[uid]

def is_bot_off(user_id):
    if user_id != ADMIN_ID and not bot_status.get("active", True):
        return True
    return False

def delayed_delete(chat_id, message_id, delay=30):
    def target():
        time.sleep(delay)
        try: bot.delete_message(chat_id, message_id)
        except: pass
    threading.Thread(target=target).start()

# کیبورد انتخاب زبان
def lang_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🇦🇫 دری / فارسی", callback_data="setlang_fa"),
        types.InlineKeyboardButton("🇦🇫 پښتو", callback_data="setlang_ps"),
        types.InlineKeyboardButton("🇺🇸 English", callback_data="setlang_en")
    )
    return markup

def main_keyboard(lang):
    if not lang: lang = "fa"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton(LANG_TEXTS["btn_apps"][lang]))
    markup.row(types.KeyboardButton(LANG_TEXTS["btn_links"][lang]))
    markup.row(types.KeyboardButton(LANG_TEXTS["btn_daily"][lang]), types.KeyboardButton(LANG_TEXTS["btn_support"][lang]))
    markup.row(types.KeyboardButton(LANG_TEXTS["btn_myinfo"][lang]), types.KeyboardButton(LANG_TEXTS["btn_buy"][lang]))
    markup.row(types.KeyboardButton(LANG_TEXTS["btn_changelang"][lang]))
    return markup

def apps_keyboard(lang):
    if not lang: lang = "fa"
    markup = types.InlineKeyboardMarkup(row_width=1)
    for item_id, info in bot_items.items():
        if info["type"] == "file":
            name = info["name"][lang] if isinstance(info["name"], dict) else info["name"]
            pt_str = "امتیاز" if lang == "fa" else ("امتیازونه" if lang == "ps" else "Points")
            markup.add(types.InlineKeyboardButton(f"{name} | {info['points']} {pt_str}", callback_data=f"ask_{item_id}"))
    return markup

def links_keyboard(lang):
    if not lang: lang = "fa"
    markup = types.InlineKeyboardMarkup(row_width=1)
    for item_id, info in bot_items.items():
        if info["type"] == "link":
            name = info["name"][lang] if isinstance(info["name"], dict) else info["name"]
            pt_str = "امتیاز" if lang == "fa" else ("امتیازونه" if lang == "ps" else "Points")
            markup.add(types.InlineKeyboardButton(f"{name} | {info['points']} {pt_str}", callback_data=f"ask_{item_id}"))
    return markup

@bot.message_handler(commands=['turn'])
def toggle_bot(message):
    if message.from_user.id != ADMIN_ID: return
    bot_status["active"] = not bot_status.get("active", True)
    save_status()
    status_str = "🟢 روشن و فعال" if bot_status["active"] else "🔴 خاموش (آف)"
    bot.reply_to(message, f"⚙️ وضعیت ربات تغییر یافت به: {status_str}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if is_bot_off(user_id):
        bot.reply_to(message, "❌ ربات در حال حاضر خاموش است.")
        return
    parts = message.text.split()
    is_new = str(user_id) not in users_db
    user_data = get_user_data(user_id)
    if is_new and len(parts) > 1 and parts[1].isdigit() and int(parts[1]) != user_id:
        referrer_id = int(parts[1])
        ref_data = get_user_data(referrer_id)
        user_data["referred_by"] = referrer_id
        ref_data["points"] += 2
        ref_data["referrals_count"] = ref_data.get("referrals_count", 0) + 1
        save_db()
        try: bot.send_message(referrer_id, "🎉 یک کاربر از طریق لینک شما وارد شد و 2 امتیاز دریافت کردید!")
        except: pass
    if not user_data["lang"]:
        bot.send_message(user_id, LANG_TEXTS["select_lang"], reply_markup=lang_keyboard())
    else:
        lang = user_data["lang"]
        bot.reply_to(message, LANG_TEXTS["welcome"][lang], reply_markup=main_keyboard(lang))

@bot.message_handler(commands=['setpoint'])
def set_user_points(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        parts = message.text.split()
        if len(parts) == 3:
            target_id = int(parts[1])
            points_change = int(parts[2])
            user_data = get_user_data(target_id)
            old_points = user_data["points"]
            user_data["points"] += points_change
            if user_data["points"] < 0: user_data["points"] = 0
            new_points = user_data["points"]
            save_db()
            bot.reply_to(message, f"🟢 **عملیات موفقیت‌آمیز بود!**\n\n🆔 کاربر: `{target_id}`\n📥 تغییرات: {points_change:+} امتیاز\n💰 امتیاز قبلی: {old_points}\n💳 امتیاز جدید: {new_points}", parse_mode="Markdown")
            try:
                sign_str = "افزایش" if points_change >= 0 else "کاهش"
                change_abs = abs(points_change)
                notify_msg = f"🔔 **اطلاعیه حساب شما:**\n\n" \
                             f"👤 کاربر گرامی، حساب شما توسط **مدیریت (رئیس شاهد)** تغییر یافت:\n\n" \
                             f"📊 نوع تغییر: **{sign_str} امتیاز**\n" \
                             f"📥 مقدار تغییر: `{change_abs}` امتیاز\n" \
                             f"💰 امتیاز قبلی شما: `{old_points}`\n" \
                             f"💳 کل امتیاز فعلی شما: **{new_points} امتیاز**\n\n" \
                             f"🌹 تشکر از همراهی شما با ما."
                bot.send_message(target_id, notify_msg, parse_mode="Markdown")
            except: pass
    except Exception as e:
        bot.reply_to(message, "🔴 **خطا در انجام عملیات!**")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID: return
    total_users = len(users_db)
    current_state = "🟢 روشن و فعال" if bot_status.get("active", True) else "🔴 خاموش (آف شده)"
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📝 ارسال پیام دلخواه به همه", callback_data="admin_broadcast"),
        types.InlineKeyboardButton("🔄 فوروارد پیام به همه", callback_data="admin_forward")
    )
    panel_text = f"📊 **منوی مدیریت رئیس شاهد:**\n\n🟢 کل کاربران فعال: **{total_users} نفر**\n🔴 وضعیت کنونی سیستم: **{current_state}**"
    bot.reply_to(message, panel_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    if is_bot_off(user_id):
        bot.answer_callback_query(call.id, "❌ ربات خاموش است.", show_alert=True)
        return
    user_data = get_user_data(user_id)
    lang = user_data["lang"] if user_data["lang"] else "fa"

    # پردازش انتخاب زبان
    if call.data.startswith("setlang_"):
        selected_lang = call.data.replace("setlang_", "")
        user_data["lang"] = selected_lang
        save_db()
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, LANG_TEXTS["welcome"][selected_lang], reply_markup=main_keyboard(selected_lang))
        bot.answer_callback_query(call.id, "Language updated / ژبه بدله شوه")
        return

    if call.data.startswith("admin_") and user_id == ADMIN_ID:
        if call.data == "admin_broadcast":
            user_state[user_id] = "waiting_broadcast"
            bot.send_message(user_id, "✍️ لطفاً متن پیام خود را بفرستید:")
            bot.answer_callback_query(call.id)
        elif call.data == "admin_forward":
            user_state[user_id] = "waiting_forward"
            bot.send_message(user_id, "↩️ لطفاً پیام خود را اینجا فوروارد کنید:")
            bot.answer_callback_query(call.id)
        return

    if call.data.startswith("ask_"):
        item_id = call.data.replace("ask_", "")
        if item_id in bot_items:
            item = bot_items[item_id]
            name = item["name"][lang] if isinstance(item["name"], dict) else item["name"]
            markup = types.InlineKeyboardMarkup()
            markup.row(
                types.InlineKeyboardButton("✅ Yes / بله", callback_data=f"buy_{item_id}"),
                types.InlineKeyboardButton("❌ No / لغو", callback_data="cancel_buy")
            )
            ask_msg = LANG_TEXTS["ask_buy"][lang].format(name, item["points"])
            bot.send_message(user_id, ask_msg, reply_markup=markup, parse_mode="Markdown")
            bot.answer_callback_query(call.id)
        return

    if call.data == "cancel_buy":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id, "Canceled.")
        return

    if call.data.startswith("buy_"):
        item_id = call.data.replace("buy_", "")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        if item_id in bot_items:
            item = bot_items[item_id]
            if user_data["points"] >= item["points"]:
                user_data["points"] -= item["points"]
                save_db()
                bot.answer_callback_query(call.id, "📥 Sending...")
                sent_msg = None
                if item["type"] == "file":
                    caption_text = item.get("caption", "✅ Product") + LANG_TEXTS["security_warn"][lang]
                    try: sent_msg = bot.send_document(user_id, item["file_id"], caption=caption_text)
                    except: bot.send_message(user_id, "Error sending file.")
                elif item["type"] == "link":
                    msg_text = f"🔗 {item['username']}" + LANG_TEXTS["security_warn"][lang]
                    sent_msg = bot.send_message(user_id, msg_text)
                if sent_msg:
                    delayed_delete(user_id, sent_msg.message_id, 30)
            else:
                bot.answer_callback_query(call.id, LANG_TEXTS["insufficient_points"][lang], show_alert=True)

# دریافت شناسه فایل‌ها فقط برای ادمین (رئیس شاهد)
@bot.message_handler(content_types=['document', 'photo', 'video', 'audio'], func=lambda message: message.from_user.id == ADMIN_ID)
def get_file_id(message):
    file_id = None
    file_type = ""
    
    if message.document:
        file_id = message.document.file_id
        file_type = "Document / App"
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_type = "Photo"
    elif message.video:
        file_id = message.video.file_id
        file_type = "Video"
    elif message.audio:
        file_id = message.audio.file_id
        file_type = "Audio"

    if file_id:
        text_reply = f"🟢 **فایل با موفقیت دریافت شد!**\n\n" \
                     f"📁 نوع فایل: `{file_type}`\n" \
                     f"🆔 شناسه فایل (`file_id`):\n`{file_id}`\n\n" \
                     f"⚠️ این متن را کپی کنید و در دیتابیس ربات قرار دهید."
        bot.reply_to(message, text_reply, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'document', 'voice', 'video'])
def handle_all_messages(message):
    user_id = message.from_user.id
    text = message.text if message.text else ""

    if user_id == ADMIN_ID and message.reply_to_message:
        try:
            first_line = message.reply_to_message.text if message.reply_to_message.text else message.reply_to_message.caption
            target_user_id = int(first_line.split("\n")[0].replace("📥 پیام از کاربر: ", ""))
            bot.send_message(target_user_id, f"📥 **پاسخ پشتیبانی (رئیس شاهد):**\n\n{text}")
            bot.reply_to(message, "✅ ارسال شد.")
            return
        except: pass

    if is_bot_off(user_id): return
    user_data = get_user_data(user_id)
    lang = user_data["lang"]

    if text in ["🌐 تغییر زبان / ژبه بدلول / Change Language", "/lang"]:
        bot.send_message(user_id, LANG_TEXTS["select_lang"], reply_markup=lang_keyboard())
        return

    if not lang:
        bot.send_message(user_id, LANG_TEXTS["select_lang"], reply_markup=lang_keyboard())
        return

    if user_id == ADMIN_ID and user_state.get(user_id) in ["waiting_broadcast", "waiting_forward"]:
        state = user_state.get(user_id)
        del user_state[user_id]
        bot.send_message(user_id, "⏳ در حال ارسال...")
        for uid in list(users_db.keys()):
            try:
                if state == "waiting_broadcast": bot.send_message(int(uid), text)
                else: bot.forward_message(int(uid), message.chat.id, message.message_id)
                time.sleep(0.05)
            except: pass
        bot.send_message(user_id, "📢 پایان ارسال همگانی.")
        return

    if user_state.get(user_id) == "waiting_support":
        del user_state[user_id]
        info_header = f"📥 پیام از کاربر: {user_id}\n👤 نام: {message.from_user.first_name}\n\n💬 متن: {text}"
        bot.send_message(ADMIN_ID, info_header)
        bot.send_message(user_id, LANG_TEXTS["support_success"][lang], reply_markup=main_keyboard(lang))
        return

    if text == LANG_TEXTS["btn_apps"][lang]:
        bot.send_message(user_id, "👇 Apps / برنامه‌ها:", reply_markup=apps_keyboard(lang))
    elif text == LANG_TEXTS["btn_links"][lang]:
        bot.send_message(user_id, "👇 Links / ربات‌ها:", reply_markup=links_keyboard(lang))
    elif text == LANG_TEXTS["btn_daily"][lang]:
        current_time = time.time()
        last_daily = user_data.get("last_daily")
        if last_daily is None or (current_time - last_daily) >= 86400:
            user_data["points"] += 2
            user_data["last_daily"] = current_time
            save_db()
            bot.send_message(user_id, LANG_TEXTS["daily_success"][lang])
        else:
            bot.send_message(user_id, LANG_TEXTS["daily_fail"][lang])
    elif text == LANG_TEXTS["btn_buy"][lang]:
        if lang == "fa":
            p_text = "💳 ** تعرفه خرید امتیاز:**\n\n🔹 50 امتیاز ➔ 100 افغانی\n🔹 200 امتیاز ➔ 350 افغانی\n\nجهت خرید به پشتیبانی پیام دهید."
        elif lang == "ps":
            p_text = "💳 **د امتیازانو پېرلو بیې:**\n\n🔹 50 امتیازونه ➔ 100 افغانۍ\n🔹 200 امتیازونه ➔ 350 افغانۍ\n\nد پېرلو لپاره ملاتړ ته پیغام واستوئ."
        else:
            p_text = "💳 **Price List:**\n\n🔹 50 Points ➔ 100 AFN\n🔹 200 Points ➔ 350 AFN\n\nPlease message support to buy."
        bot.send_message(user_id, p_text, parse_mode="Markdown")
    elif text == LANG_TEXTS["btn_support"][lang]:
        user_state[user_id] = "waiting_support"
        bot.send_message(user_id, LANG_TEXTS["support_msg"][lang], reply_markup=types.ReplyKeyboardRemove())
    elif text == LANG_TEXTS["btn_myinfo"][lang]:
        bot_info = bot.get_me()
        invite_link = f"https://t.me/{bot_info.username}?start={user_id}"
        referrals = user_data.get("referrals_count", 0)
        if lang == "fa":
            info_text = f"📊 **اطلاعات حساب شما:**\n\n💰 امتیاز فعلی: **{user_data['points']}**\n👥 تعداد دعوت‌ها: **{referrals} نفر**\n\n🔗 لینک دعوت:\n{invite_link}"
        elif lang == "ps":
            info_text = f"📊 **ستاسو د حساب معلومات:**\n\n💰 اوسني امتیازونه: **{user_data['points']}**\n👥 د بلنو شمیر: **{referrals} کسان**\n\n🔗 د بلنې لینک:\n{invite_link}"
        else:
            info_text = f"📊 **Account Info:**\n\n💰 Current Points: **{user_data['points']}**\n👥 Total Invites: **{referrals}**\n\n🔗 Referral Link:\n{invite_link}"
        bot.send_message(user_id, info_text, parse_mode="Markdown")

if __name__ == "__main__":
    while True:
        try: bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except KeyboardInterrupt: break
        except: time.sleep(5)

