import flask
import threading
import os

app = flask.Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# استدعاء الدالة لتبدأ العمل في الخلفية
keep_alive()


import telebot
import requests

# --- ضع بياناتك هنا ---
API_TOKEN = '8606759947:AAEsGFSIgle1QtDEyFg3TnUgKjscEsxYXy4'
REMOVE_BG_API_KEY = '1D9ovW36BttGh9ykVCxruD8w'
# ----------------------

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        msg = bot.reply_to(message, "⏳ جاري إزالة الخلفية بجودة عالية... انتظر ثواني")
        
        # الحصول على رابط الصورة
        file_info = bot.get_file(message.photo[-1].file_id)
        file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"
        
        # إرسال الصورة للموقع لمعالجتها
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            data={'image_url': file_url, 'size': 'auto'},
            headers={'X-API-Key': REMOVE_BG_API_KEY},
        )
        
        if response.status_code == requests.codes.ok:
            # إرسال النتيجة كملف PNG
            bot.send_document(message.chat.id, response.content, visible_file_name='no-bg.png')
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.reply_to(message, "⚠️ حدث خطأ، تأكد من الـ API Key أو الرصيد.")
            
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ: {e}")

print("✅ البوت شغال الآن بطريقة الـ API الذكية والسريعة...")
bot.polling()

