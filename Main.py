
import os
import requests
import telebot

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not TELEGRAM_TOKEN or not GROQ_API_KEY:
    raise RuntimeError(
        "Please configure TELEGRAM_TOKEN and GROQ_API_KEY"
    )

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "سلام داداش! ⚡️ من Turboie هستم؛ "
        "دستیار هوشمند تو. هر چی می‌خوای بپرس! 🤖"
    )

@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are Turboie, a helpful AI assistant. "
                            "Reply in the user's language. "
                            "Be friendly, accurate and concise."
                        ),
                    },
                    {"role": "user", "content": message.text or ""},
                ],
                "temperature": 0.7,
            },
            timeout=60,
        )

        if response.ok:
            answer = response.json()["choices"][0]["message"]["content"]
            bot.reply_to(message, answer[:4000] or "داداش، دوباره بپرس! ❤️")
        else:
            print("Groq error:", response.status_code, response.text)
            bot.reply_to(
                message,
                "داداش، اتصال هوش مصنوعی مشکل داره. کمی بعد دوباره امتحان کن! ❤️"
            )

    except Exception as error:
        print("Error:", repr(error))
        bot.reply_to(
            message,
            "داداش، یه خطای موقت پیش اومده. دوباره امتحان کن! ⚡️"
        )

print("Turboie is running!")
bot.infinity_polling(skip_pending=True)
