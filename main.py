import requests
import time
import statistics
from keep_alive import keep_alive
from bs4 import BeautifulSoup

TOKEN = "7310358399:AAGJvaTRwrTS1olXfoHxQ0SiS31jvFg9JzI"
CHAT_ID = 1704060687
SITE_URL = "https://ais.usvisa-info.com/en-tr/niv"

last_10_latencies = []

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def check_latency():
    try:
        start_time = time.time()
        response = requests.get(SITE_URL, timeout=10)
        latency = round((time.time() - start_time) * 1000)

        last_10_latencies.append(latency)
        if len(last_10_latencies) > 10:
            last_10_latencies.pop(0)

        avg_latency = round(statistics.mean(last_10_latencies))

        if avg_latency > 1500:
            yorum = "🔴 AŞIRI YOĞUNLUK — Açılma olasılığı yüksek!"
        elif avg_latency > 800:
            yorum = "🟠 Orta yoğunluk"
        else:
            yorum = "🟢 Sistem sakin"

        msg = f"""⏱️ Ping Takibi
Anlık Gecikme: {latency} ms
📊 Son 10 Ortalama: {avg_latency} ms
🧠 Yorum: {yorum}"""

        send_telegram_message(msg)

    except Exception as e:
        send_telegram_message(f"❗ Ping kontrolü hatası: {e}")

def check_site():
    try:
        response = requests.get(SITE_URL, timeout=10)
        if "no appointments available" in response.text.lower():
            slot_status = "❌ Randevu bulunamadı."
        elif "available" in response.text.lower():
            slot_status = "✅ RANDEVU AÇILMIŞ OLABİLİR!"
        else:
            slot_status = "🤖 Slot bilgisi analiz edilemiyor."

        send_telegram_message(f"📅 Slot Durumu Güncellemesi:\n{slot_status}")

    except Exception as e:
        send_telegram_message(f"❗ Slot kontrol hatası: {e}")

def check_news():
    try:
        news_feed_url = "https://news.google.com/rss/search?q=us+visa+appointment+turkey"
        resp = requests.get(news_feed_url)
        soup = BeautifulSoup(resp.text, "xml")
        items = soup.find_all("item")
        for item in items[:1]:
            title = item.title.text
            link = item.link.text
            send_telegram_message(f"📰 Haber Takibi:\n{title}\n{link}")
    except Exception as e:
        send_telegram_message(f"❗ Haber hatası: {e}")

def check_twitter_simulation():
    try:
        keywords = ["randevu açıldı", "slot available", "student visa opened"]
        fake_tweet = "Hi everyone, US student visa slots are now open in Ankara!"  # simülasyon
        if any(kw in fake_tweet.lower() for kw in keywords):
            send_telegram_message(f"🐦 Twitter Simülasyonu:\n⚠️ {fake_tweet}")
    except Exception as e:
        send_telegram_message(f"❗ Twitter hatası: {e}")

# SUNUCU AKTİF TUT
keep_alive()

counter = 0

while True:
    check_latency()  # her dakika
    if counter % 5 == 0:  # her 5 dakikada bir
        check_site()
        check_news()
        check_twitter_simulation()
    counter += 1
    time.sleep(60)  # her döngü 1 dakika
