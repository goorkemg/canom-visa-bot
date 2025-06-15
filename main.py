import requests
import time

# Telegram bilgileri
TOKEN = "7310358399:AAGJvaTRwrTS1olXfoHxQ0SiS31jvFg9JzI"
CHAT_ID = 1704060687

URL = "https://tr.usembassy.gov/visas/"
notified = False
ping_list = []

def check_vize_durumu():
    try:
        start = time.time()
        response = requests.get(URL, timeout=15)
        end = time.time()
        ping = int((end - start) * 1000)
        ping_list.append(ping)

        # Sadece son 10 ping'i tut
        if len(ping_list) > 10:
            ping_list.pop(0)

        # Sayfa açıldı mı?
        acildi = "coming soon" not in response.text.lower()
        return acildi, ping

    except Exception as e:
        print("Hata:", e)
        return False, 9999

def yorum_yap(ping_ort):
    if ping_ort < 300:
        return "🟢 Sistem sakin"
    elif ping_ort < 800:
        return "🟠 Yoğunluk orta"
    else:
        return "🔴 Sistem aşırı yoğun"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

i = 0
while True:
    vize_acik, ping = check_vize_durumu()
    i += 1

    # 5 dakikada bir özet mesaj gönder
    if i % 5 == 0:
        ort_ping = int(sum(ping_list) / len(ping_list)) if ping_list else 9999
        yorum = yorum_yap(ort_ping)
        durum = "🟢 UYARI KALKTI! Açılmış olabilir, lütfen kontrol et!" if vize_acik else "🔴 Uyarı hâlâ duruyor. Henüz açılmamış olabilir."

        mesaj = f"""📡 Güncelleme (Her 5 dk bir):
{durum}
⏱️ Ping Ortalama (Son 5 dk): {ort_ping} ms
🧠 Yorum: {yorum}
"""
        send_telegram(mesaj)

    if not notified and vize_acik:
        send_telegram("📢 VİZE BAŞVURULARI AÇILDI! 👉 https://ais.usvisa-info.com")
        notified = True

    time.sleep(60)  # 1 dakikada bir ping ölçümü
