import requests
import time
from keep_alive import keep_alive

TOKEN = "7310358399:AAGJvaTRwrTS1olXfoHxQ0SiS31jvFg9JzI"
CHAT_ID = 1704060687
URL = "https://www.ustraveldocs.com/tr/tr-niv-appointments.asp"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram'a mesaj gönderilemedi: {e}")

def check_website():
    try:
        response = requests.get(URL)
        content = response.text

        # ❗ Sayfa içeriğini Telegram'da gönder (ilk 1000 karakter)
        snippet = content[:1000]
        send_telegram_message("📄 Sayfa içeriği (ilk 1000 karakter):\n\n" + snippet)

    except Exception as e:
        send_telegram_message(f"❌ Siteye bağlanılamadı: {e}")

keep_alive()

while True:
    check_website()
    time.sleep(300)  # 5 dakika
