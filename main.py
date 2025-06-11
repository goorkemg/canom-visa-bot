import requests
import time
from keep_alive import keep_alive

TOKEN = "7310358399:AAGJvaTRwrTS1olXfoHxQ0SiS31jvFg9JzI"
CHAT_ID = 1704060687
URL = "https://www.ustraveldocs.com/tr/tr-niv-appointments.asp"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html"
}

response_times = []  # Son 10 ölçümü tutmak için

def send_telegram_message(message):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": message}
        )
    except Exception as e:
        print(f"Telegram mesajı gönderilemedi: {e}")

def analyze_response_time(rt_ms):
    global response_times

    # Listeyi 10 elemana sabitle
    response_times.append(rt_ms)
    if len(response_times) > 10:
        response_times.pop(0)

    avg = sum(response_times) / len(response_times)
    fark = rt_ms - avg
    fark_yuzde = (fark / avg) * 100

    # Yorum üret
    if rt_ms < 800:
        durum = "🟢 Düşük yoğunluk. Sistem sakin."
        olasilik = "❌ Açılma ihtimali düşük."
    elif rt_ms < 1400:
        durum = "🟡 Orta yoğunluk. Sistemde hareket olabilir."
        olasilik = "⚠️ Açılma ihtimali var, dikkatli ol."
    else:
        durum = "🔴 Yüksek yoğunluk! Sistem zorlanıyor."
        olasilik = "✅ Açılma ihtimali yüksek. Hemen hazır ol!"

    mesaj = f"""✅ Siteye erişildi.
Yanıt süresi: {rt_ms} ms
📊 Son 10 ortalama: {int(avg)} ms
📈 Gecikme: {'+' if fark >= 0 else ''}{int(fark_yuzde)}%
{durum}
{olasilik}"""

    return mesaj

def check_site():
    try:
        start = time.time()
        response = requests.get(URL, headers=HEADERS, timeout=15)
        end = time.time()

        if response.status_code == 200:
            rt_ms = int((end - start) * 1000)
            yorum = analyze_response_time(rt_ms)
            send_telegram_message(yorum)
        else:
            send_telegram_message(f"⚠️ HTTP Hata: {response.status_code}")
    except Exception as e:
        send_telegram_message(f"❌ Hata oluştu: {e}")

keep_alive()

while True:
    check_site()
    time.sleep(60)  # 1 dakikada bir çalıştır
