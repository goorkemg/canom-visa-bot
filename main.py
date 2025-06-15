import requests
import time
from bs4 import BeautifulSoup
from keep_alive import keep_alive

# Telegram bot bilgileri
TOKEN = "7310358399:AAGJvaTRwrTS1olXfoHxQ0SiS31jvFg9JzI"
CHAT_ID = 1704060687
URL = "https://tr.usembassy.gov/visas/"
ping_results = []

# 🟢 Ping fonksiyonu – optimize edilmiş hali
def ping_site():
    try:
        start = time.time()
        response = requests.get(URL, timeout=5, allow_redirects=False, stream=False)
        end = time.time()
        if response.status_code in [200, 301, 302]:
            return round((end - start) * 1000)
        else:
            return -1
    except requests.exceptions.RequestException:
        return -1

# 🔍 Site içeriğini kontrol eden fonksiyon
def check_embassy_notice_advanced():
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        body_text = soup.get_text().lower()

        keywords = [
            "visas",
            "select a u.s. embassy or consulate",
            "transition to new appointment platform",
            "immigrant visa",
            "nonimmigrant visa"
        ]

        missing = [word for word in keywords if word not in body_text]
        if len(missing) >= 3:
            return f"⚠️ Sayfa eksik veya ağır şekilde kırpılmış olabilir. (Eksik: {', '.join(missing)})"
        else:
            return "🟢 UYARI KALKTI! Açılmış olabilir, lütfen kontrol et!"
    except Exception as e:
        return f"⚠️ Hata oluştu: {str(e)}"

# 🧠 Ping yorum fonksiyonu
def yorumla_ping(ping_avg):
    if ping_avg < 300:
        return "🟢 Sistem sakin"
    elif ping_avg < 800:
        return "🟠 Yoğunluk yüksek, dikkatli ol"
    else:
        return "🔴 Aşırı yoğunluk, sayfa çökmüş olabilir"

# 📩 Telegram mesaj gönderici
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, data=payload)
    except:
        pass

# 🔁 Ana döngü fonksiyonu
def run_bot():
    counter = 0
    while True:
        # 1. Ping ölç
        ping = ping_site()
        if ping != -1:
            ping_results.append(ping)
            if len(ping_results) > 5:
                ping_results.pop(0)

        # 2. Her 5 dk'da bir detaylı kontrol
        if counter % 5 == 0:
            ping_avg = sum(ping_results) / len(ping_results) if ping_results else 0
            yorum = yorumla_ping(ping_avg)

            if ping_avg > 1500:
                notice_status = "⚠️ Sistem çok yavaş, içerik kontrolü atlandı."
            else:
                notice_status = check_embassy_notice_advanced()

            msg = (
                "📡 Güncelleme (Her 5 dk bir):\n"
                f"{notice_status}\n"
                f"⏱️ Ping Ortalama (Son 5 dk): {int(ping_avg)} ms\n"
                f"🧠 Yorum: {yorum}"
            )
            send_telegram_message(msg)

        counter += 1
        time.sleep(60)

# 🔧 Keep alive ve başlat
keep_alive()
run_bot()
