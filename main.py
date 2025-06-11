import requests
import time
from keep_alive import keep_alive

TOKEN = "7310358399:AAGJvaTRwrTS1olXfoHxQ0SiS31jvFg9JzI"
CHAT_ID = 1704060687

URL = "https://ais.usvisa-info.com/en-tr/niv/schedule/40816252/appointment/days/108.json?appointments[expedite]=false"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

def send_telegram_message(message):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": message})

def check_slots():
    try:
        r = requests.get(URL, headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()
            if data:
                slot_dates = [d['date'] for d in data]
                message = "📅 🎉 RANDEVU BULUNDU!\n" + "\n".join(slot_dates)
                send_telegram_message(message)
            else:
                print("❌ Slot yok")
        else:
            send_telegram_message(f"⚠️ HTTP Hata: {r.status_code}")
    except Exception as e:
        send_telegram_message(f"❌ Hata oluştu: {e}")

keep_alive()
while True:
    check_slots()
    time.sleep(300)
