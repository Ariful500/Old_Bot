import os
import time
import requests

TG_TOKEN = os.environ["TELEGRAM_TOKEN"]

MOVED_TEXT = (
    "🔴 <b>Bot Moved! | বট পরিবর্তন হয়েছে!</b>\n"
    "━━━━━━━━━━━━━━━\n"
    "❌ This bot is no longer active.\n"
    "⭐ We have launched a new & better bot!\n"
    "👉 Switch now to continue using our service.\n"
    "━━━━━━━━━━━━━━━\n"
    "❌ এই বটটি আর সক্রিয় নেই।\n"
    "⭐ আমরা নতুন ও আরো উন্নত বট চালু করেছি!\n"
    "👉 সেবা পেতে এখনই নতুন বটে যান।\n"
    "━━━━━━━━━━━━━━━"
)

MOVED_MARKUP = {
    "inline_keyboard": [[
        {"text": "🚀 Open New Bot | নতুন বট খুলুন", "url": "https://t.me/LAMIXSMS0Bot"}
    ]]
}

OFFSET = 0
RUN_DURATION = 6 * 60 * 60 - 60


def get_updates(offset):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/getUpdates"
    try:
        r = requests.get(url, params={"offset": offset, "timeout": 30}, timeout=35)
        return r.json().get("result", [])
    except:
        return []


def send_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass


def answer_callback(callback_id):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/answerCallbackQuery"
    try:
        requests.post(url, json={"callback_query_id": callback_id}, timeout=10)
    except:
        pass


def main():
    global OFFSET
    start_time = time.time()
    print("✅ Old bot redirect চালু হয়েছে।")

    while True:
        if time.time() - start_time >= RUN_DURATION:
            print("⏰ ৬ ঘন্টা সম্পন্ন। বন্ধ হচ্ছে।")
            break

        updates = get_updates(OFFSET)

        for update in updates:
            OFFSET = update["update_id"] + 1

            # Callback query হলে
            if "callback_query" in update:
                cb = update["callback_query"]
                answer_callback(cb["id"])
                chat_id = cb["message"]["chat"]["id"]
                send_message(chat_id, MOVED_TEXT, MOVED_MARKUP)
                continue

            # যেকোনো message হলে
            msg = update.get("message", {})
            if not msg:
                continue

            chat_id = msg["chat"]["id"]
            send_message(chat_id, MOVED_TEXT, MOVED_MARKUP)

        time.sleep(2)


if __name__ == "__main__":
    main()
  
