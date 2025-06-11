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
        start = time.time()
        response = requests.get(URL)
        elapsed = time.time() - start
        ms = round(elapsed * 1000)

        if response.status_code == 200:
            message = f"✅ Konsolosluk sitesi erişildi.\nYanıt süresi: {ms} ms"
        else:
            message = f"⚠️ HTTP Hatası: {response.status_code}"

        if ms > 1200:
            message += "\n⚠️ Sistem çok yavaş olabilir!"

        send_telegram_message(message)

    except Exception as e:
        send_telegram_message(f"❌ Siteye bağlanılamadı: {e}")

keep_alive()

while True:
    check_website()
    time.sleep(300)  # 5 dakika
