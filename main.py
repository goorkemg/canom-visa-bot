import requests
import time
from keep_alive import keep_alive

TOKEN = "7310358399:AAGJvaTRwrTS1olXfoHxQ0SiS31jvFg9JzI"
CHAT_ID = 1704060687

URL = "https://ais.usvisa-info.com/en-tr/niv"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html"
}

def send_telegram_message(message):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": message}
        )
    except Exception as e:
        print(f"Telegram mesajı gönderilemedi: {e}")

def check_site():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            content = response.text.lower()

            if "no appointments available" in content:
                print("❌ Slot yok.")
            elif "available appointment" in content or "appointments available" in content:
                send_telegram_message("🎉📅 RANDEVU BULUNMUŞ OLABİLİR!\nHemen kontrol et canom 💥")
            else:
                print("🔍 Anahtar kelime bulunamadı.")
        else:
            send_telegram_message(f"⚠️ HTTP HATA: {response.status_code}")
    except Exception as e:
        send_telegram_message(f"❌ HATA OLUŞTU: {e}")

keep_alive()

while True:
    check_site()
    time.sleep(300)  # Her 5 dakikada bir
