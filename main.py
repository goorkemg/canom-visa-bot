from keep_alive import keep_alive
import requests
import time
from bs4 import BeautifulSoup

# === KULLANICI BİLGİLERİ ===
TOKEN = "7310358399:AAGJvaTRwrTS1olXfoHxQ0SiS31jvFg9JzI"
CHAT_ID = 1704060687

# === VİZE SAYFASI ===
URL = "https://tr.usembassy.gov/visas/"
KEY_PHRASE = "Appointment scheduling platform coming soon"
ADDITIONAL_REQUIRED_TEXTS = [
    "visas",
    "select a u.s. embassy or consulate",
    "transition to new appointment platform",
    "immigrant visa",
    "nonimmigrant visa"
]

# === PING VERİLERİ ===
ping_results = []

# === TELEGRAM MESAJ GÖNDERME ===
def send_telegram_message(message):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": message},
            timeout=5
        )
    except Exception as e:
        print(f"Telegram gönderim hatası: {e}")

# === PING DEĞERİNİ YORUMLA ===
def yorumla_ping(ms):
    if ms < 200:
        return "🟢 Sistem sakin"
    elif ms < 400:
        return "🟡 Orta yoğunluk"
    elif ms < 800:
        return "🟠 Yoğunluk yüksek, dikkatli ol"
    else:
        return "🔴 Sistem çok yavaş! Açılma ihtimali olabilir"

# === UYARI VAR MI KONTROL ET (GELİŞMİŞ) ===
def check_embassy_notice_advanced():
    try:
        response = requests.get(URL, timeout=15)
        if response.status_code != 200:
            return "⚠️ Sayfaya erişilemedi (HTTP " + str(response.status_code) + ")"

        content = response.text
        soup = BeautifulSoup(content, "html.parser")
        page_text = soup.get_text().lower()

        if "<html" not in content.lower() or "<!doctype html" not in content.lower():
            return "⚠️ Sayfa eksik yüklenmiş olabilir, HTML tam değil."

        missing_keywords = [kw for kw in ADDITIONAL_REQUIRED_TEXTS if kw not in page_text]
        if len(missing_keywords) >= 3:
            return "⚠️ Sayfa eksik veya ağır şekilde kırpılmış olabilir. (Eksik: " + ", ".join(missing_keywords) + ")"

        if KEY_PHRASE.lower() in page_text:
            return f"🟡 Uyarı hâlâ duruyor.\n💬 Mesaj: \"{KEY_PHRASE}\""
        else:
            return "🟢 UYARI KALKTI! Sayfa tam yüklendi ve uyarı görünmüyor. Lütfen kontrol et!"
    except Exception as e:
        return f"❌ Kontrol sırasında hata oluştu: {e}"

# === PING ÖLÇÜMÜ ===
def ping_site():
    try:
        start = time.time()
        response = requests.get(URL, timeout=10)
        end = time.time()
        if response.status_code == 200:
            return round((end - start) * 1000)
        else:
            return -1
    except:
        return -1

# === ANA FONKSİYON: 5 DAKİKADA BİR KONTROL ET ===
def run_bot():
    counter = 0
    while True:
        # 1. Ping ölç
        ping = ping_site()
        if ping != -1:
            ping_results.append(ping)
            if len(ping_results) > 5:
                ping_results.pop(0)

        # 2. Her 5 dakikada bir içerik kontrolü yap
        if counter % 5 == 0:
            ping_avg = sum(ping_results) / len(ping_results) if ping_results else 0
            yorum = yorumla_ping(ping_avg)

            # 3. Ping çok yüksekse içerik kontrolü yapma
            if ping_avg > 1500:
                notice_status = "⚠️ Sistem çok yavaş, içerik kontrolü atlandı."
            else:
                notice_status = check_embassy_notice_advanced()

            # 4. Mesajı gönder
            msg = (
                "📡 Güncelleme (Her 5 dk bir):\n"
                f"{notice_status}\n"
                f"⏱️ Ping Ortalama (Son 5 dk): {int(ping_avg)} ms\n"
                f"🧠 Yorum: {yorum}"
            )
            send_telegram_message(msg)

        counter += 1
        time.sleep(60)

# === BAŞLAT ===
if __name__ == "__main__":
    keep_alive()
    run_bot()
