from keep_alive import keep_alive
import requests
from bs4 import BeautifulSoup
import time

# === USER CONFIG ===
URL = "https://tr.usembassy.gov/visas/"
KEY_PHRASE = "Appointment scheduling platform coming soon"
TOKEN = "7310358399:AAGJvaTRwrTS1olXfoHxQ0SiS31jvFg9JzI"
CHAT_ID = 1704060687

ping_results = []

def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(telegram_url, data=payload, timeout=5)
    except:
        pass  # sessizce geç

def check_embassy_notice():
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code != 200:
            return "⚠️ Sayfaya erişilemedi (HTTP " + str(response.status_code) + ")"
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text().lower()
        if KEY_PHRASE.lower() in page_text:
            return f"🟡 Uyarı hâlâ duruyor.\n💬 Mesaj: \"{KEY_PHRASE}\""
        else:
            return "🟢 UYARI KALKTI! Açılmış olabilir, lütfen kontrol et!"
    except Exception as e:
        return f"❌ Hata: {e}"

def ping_site():
    try:
        start = time.time()
        response = requests.get(URL, timeout=10)
        end = time.time()
        if response.status_code == 200:
            return int((end - start) * 1000)
        else:
            return -1
    except:
        return -1

def yorumla_ping(ms):
    if ms < 200:
        return "🟢 Sistem sakin"
    elif ms < 400:
        return "🟡 Orta yoğunluk"
    elif ms < 800:
        return "🟠 Yoğunluk yüksek, dikkatli ol"
    else:
        return "🔴 Sistem çok yavaş! Açılma ihtimali olabilir"

def run_bot():
    counter = 0
    while True:
        ping = ping_site()
        if ping != -1:
            ping_results.append(ping)
            if len(ping_results) > 5:
                ping_results.pop(0)

        if counter % 5 == 0:
            ping_avg = sum(ping_results) / len(ping_results) if ping_results else 0
            yorum = yorumla_ping(ping_avg)
            notice_status = check_embassy_notice()
            msg = (
                "📡 Güncelleme (Her 5 dk bir):\n"
                f"{notice_status}\n"
                f"⏱️ Ping Ortalama (Son 5 dk): {int(ping_avg)} ms\n"
                f"🧠 Yorum: {yorum}"
            )
            send_telegram_message(msg)

        counter += 1
        time.sleep(60)

if __name__ == "__main__":
    keep_alive()
    run_bot()
