import requests

TOKEN = "7310358399:AAGJvaTRwrTS1olXfoHxQ0SiS31jvFg9JzI"
CHAT_ID = 1704060687

def send_telegram_message(message):
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": message}
        )
        print("Durum:", r.status_code)
        print("Yanıt:", r.text)
    except Exception as e:
        print("Hata:", e)

send_telegram_message("🔔 Telegram testi çalışıyor mu canom?")
