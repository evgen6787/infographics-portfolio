import telebot
from g4f.client import Client

# --- НАСТРОЙКА КЛЮЧЕЙ И ID ---
TELEGRAM_BOT_TOKEN = "8965640431:AAHVgQfVrj7HFHI2MYbCATAP4fMKwEIGsME"
YOUR_TELEGRAM_CHAT_ID = 1586057111  # Ваш личный цифровой ID (как число)

# Инициализируем бота и бесплатный клиент ChatGPT
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
ai_client = Client()

# Память контекста диалога для каждого клиента (чтобы ИИ помнил прошлые сообщения)
user_history = {}

# Инструкция, обучающая ИИ внутри Telegram-бота
SYSTEM_PROMPT = """
Ты — продвинутый ИИ-ассистент студии дизайна InfographicsAI внутри Telegram-бота. 
Твоя задача — помогать клиентам маркетплейсов отслеживать заказы, принимать от них фотографии товаров и консультировать.
Отвечай строго на РУССКОМ языке. Будь очень вежлив, дружелюбен, используй эмодзи. 
Если клиент пишет, что хочет отправить фото — скажи, чтобы он прислал их сюда прямо в чат как картинки или файлы.
Если клиент спрашивает статус заказа, вежливо ответь: "Передал ваш запрос мастеру! Прямо сейчас дизайнер собирает уникальный неоновый фон. Ожидайте уведомления прямо в этом чате!"
"""

# 1. ОБРАБОТКА КОМАНДЫ /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    username = message.from_user.username or message.from_user.first_name
    
    # Сбрасываем историю для нового диалога
    user_history[chat_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    welcome_text = f"🎉 Здравствуйте, @{username}! Рад видеть вас в официальном боте студии InfographicsAI!\n\n" \
                   f"📸 **Сюда вы можете отправить фотографии вашего товара** (файлом или обычным фото).\n\n" \
                   f"🤖 Наш ИИ-ассистент и мастер уже прорабатывают ваше ТЗ с сайта. Прямо в этом чате вы будете получать уведомления о статусе, закрывать правки и сможете скачать готовые карточки в 4K!"
    
    bot.send_message(chat_id, welcome_text)

# 2. ОБРАБОТКА ПРИСЛАННЫХ ФОТОГРАФИЙ ТОВАРА
@bot.message_handler(content_types=['photo', 'document'])
def handle_docs_photos(message):
    chat_id = message.chat.id
    username = message.from_user.username or message.from_user.first_name
    
    # Бот вежливо отвечает клиенту
    bot.send_message(chat_id, "📸 Фотографии вашего товара успешно получены и переданы дизайнеру в обработку! Спасибо!")
    
    # Бот мгновенно пересылает эти фотографии ВАМ в личные сообщения, чтобы вы их не потеряли
    notification_text = f"🔔 **КЛИЕНТ ПРИСЛАЛ ФОТО ТОВАРА!**\n👤 От: @{username} (ID: {chat_id})"
    bot.send_message(YOUR_TELEGRAM_CHAT_ID, notification_text)
    
    if message.content_type == 'photo':
        # Пересылаем самую большую версию фото
        bot.send_photo(YOUR_TELEGRAM_CHAT_ID, message.photo[-1].file_id)
    else:
        # Пересылаем как документ (без сжатия)
        bot.send_document(YOUR_TELEGRAM_CHAT_ID, message.document.file_id)

# 3. УМНЫЙ ИИ-ДИАЛОГ С КЛИЕНТАМИ И УПРАВЛЕНИЕ ДЛЯ ВАС (АДМИНА)
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    text = message.text
    username = message.from_user.username or message.from_user.first_name

    # --- РЕЖИМ АДМИНИСТРАТОРА (Для вас) ---
    # Если пишет владелец студии (вы) и сообщение начинается с команды /reply
    if chat_id == YOUR_TELEGRAM_CHAT_ID:
        if text.startswith("/reply "):
            try:
                # Пример команды: /reply 123456789 Текст вашего ответа
                parts = text.split(" ", 2)
                target_chat_id = int(parts[1])
                admin_text = parts[2]
                
                # Отправляем сообщение клиенту на сайт/в бот
                bot.send_message(target_chat_id, f"👑 **Сообщение от ИИ-Дизайнера:**\n\n{admin_text}")
                bot.send_message(YOUR_TELEGRAM_CHAT_ID, "✅ Ответ успешно доставлен клиенту!")
            except Exception as e:
                bot.send_message(YOUR_TELEGRAM_CHAT_ID, "❌ Ошибка! Неверный формат. Пишите строго так:\n`/reply ID_КЛИЕНТА Текст ответа`")
        else:
            bot.send_message(YOUR_TELEGRAM_CHAT_ID, "💡 Шеф, чтобы ответить клиенту, напишите команду:\n`/reply ID_КЛИЕНТА Ваш текст`\n\nID клиента пишется в каждом уведомлении о новом брифе!")
        return

    # --- РЕЖИМ КЛИЕНТА (Диалог с GPT-4o) ---
    # Если у пользователя еще нет истории — создаем её
    if chat_id not in user_history:
        user_history[chat_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
        
    # Добавляем реплику пользователя в память
    user_history[chat_id].append({"role": "user", "content": text})
    
    # Показываем статус "бот печатает..."
    bot.send_chat_action(chat_id, 'typing')
    
    try:
        # Бесплатно вызываем ChatGPT (GPT-4o) через g4f
        response = ai_client.chat.completions.create(
            model="gpt-4o",
            messages=user_history[chat_id]
        )
        ai_response = response.choices.message.content
    except Exception as e:
        ai_response = "Извините, я немного задумался. Наш ИИ-мастер уже на связи, вы можете задать вопрос ему напрямую в ЛС!"

    # Отправляем ответ клиенту и сохраняем его в память
    bot.send_message(chat_id, ai_response)
    user_history[chat_id].append({"role": "assistant", "content": ai_response})

# Запуск бота на бесконечные прослушивания сообщений
print("🚀 Ваш умный ИИ Telegram-бот успешно запущен и слушает команды...")
bot.infinity_polling()
