import os
import telebot
import google.generativeai as genai

# الحصول على الرموز من متغيرات البيئة للبيئة السحابية
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

# تهيئة جيميناي وبوت تيليجرام
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# معالج أمر /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أنا بوت ZekoYemen المدعوم بالذكاء الاصطناعي. كيف يمكنني مساعدتك اليوم؟")

# معالج جميع الرسائل النصية
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # إرسال مؤشر "جاري الكتابة..."
        bot.send_chat_action(message.chat.id, 'typing')
        
        # توليد الرد من نموذج جيميناي
        response = model.generate_content(message.text)
        
        # إرسال الرد للمستخدم
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "عذراً، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة لاحقاً.")

# تشغيل البوت
if __name__ == "__main__":
    print("البوت يعمل الآن...")
    bot.infinity_polling()
