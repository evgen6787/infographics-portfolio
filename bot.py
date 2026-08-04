import telebot
import os

# --- НАСТРОЙКА ТОКЕНА И ВАШЕГО ID ---
TELEGRAM_BOT_TOKEN = "8965640431:AAHVgQfVrj7HFHI2MYbCATAP4fMKwEIGsME"
YOUR_TELEGRAM_CHAT_ID = 1586057111  # Ваш личный цифровой ID (как число)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Локальная база данных прямо в оперативной памяти бота, чтобы связывать никнеймы с ID чатов
# Ключ: никнейм в нижнем регистре (без @), Значение: chat_id клиента
client_database = {}

# 1. ОБРАБОТКА КОМАНДЫ /start ДЛЯ КЛИЕНТОВ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    # Автоматически сохраняем никнейм клиента в нашу базу при старте
    username = message.from_user.username
    
    if username:
        clean_username = username.lower().strip()
        client_database[clean_username] = chat_id
        
        # Уведомляем вас, что клиент успешно подключился к боту
        notification = f"🟢 Пользователь @{username} (ID: {chat_id}) успешно запустил бота и готов к диалогу!"
        bot.send_message(YOUR_TELEGRAM_CHAT_ID, notification)
    
    welcome_text = f"🎉 Здравствуйте! Рад видеть вас в официальном боте студии InfographicsAI!\n\n" \
                   f"📸 **Сюда вы можете отправить фотографии вашего товара** (обычным фото или файлом без сжатия).\n\n" \
                   f"🤖 Наш менеджер уже изучает ваш бриф с сайта. Прямо в этом чате вы будете получать уведомления от дизайнера, обсуждать правки и сможете скачать готовые карточки в максимальном качестве!"
    
    bot.send_message(chat_id, welcome_text)

# 2. ПРИЕМ ФОТОГРАФИЙ ОТ КЛИЕНТОВ И ПЕРЕСЫЛКА ВАМ
@bot.message_handler(content_types=['photo', 'document'])
def handle_docs_photos(message):
    chat_id = message.chat.id
    username = message.from_user.username or "Скрытый_Ник"
    
    # Если фото прислали вы сами (Админ) — бот проигнорирует, чтобы не зацикливаться
    if chat_id == YOUR_TELEGRAM_CHAT_ID:
        bot.send_message(YOUR_TELEGRAM_CHAT_ID, "💡 Шеф, чтобы отправить файлы конкретному клиенту, просто перешлите их ему через команду с его никнеймом.")
        return
        
    # Сохраняем связь ника и ID на случай, если клиент не нажимал /start, а просто скинул фото
    if message.from_user.username:
        client_database[message.from_user.username.lower().strip()] = chat_id

    # Отвечаем клиенту
    bot.send_message(chat_id, "📸 Фотографии вашего товара успешно получены и переданы дизайнеру в обработку! Спасибо!")
    
    # Пересылаем файлы вам на телефон с указанием, от кого они пришли
    notification_text = f"🔔 **КЛИЕНТ ПРИСЛАЛ МАТЕРИАЛЫ ДЛЯ ДИЗАЙНА!**\n👤 От: @{username}\nℹ️ Для ответа введите: `{username} Текст вашего сообщения`"
    bot.send_message(YOUR_TELEGRAM_CHAT_ID, notification_text)
    
    if message.content_type == 'photo':
        bot.send_photo(YOUR_TELEGRAM_CHAT_ID, message.photo[-1].file_id)
    else:
        bot.send_document(YOUR_TELEGRAM_CHAT_ID, message.document.file_id)

# 3. ЦЕНТРАЛЬНЫЙ ПУЛЬТ ОБРАТНОЙ СВЯЗИ (МЕНЕДЖЕР КОМАНД)
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    text = message.text.strip()
    
    # --- РЕЖИМ АДМИНИСТРАТОРА (Ваш пульт управления) ---
    if chat_id == YOUR_TELEGRAM_CHAT_ID:
        # Проверяем, что сообщение содержит как минимум два слова (Имя_Пользователя и Текст)
        if " " in text:
            parts = text.split(" ", 1)
            target_nick = parts[0].replace("@", "").lower().strip() # Очищаем ник от собачки и пробелов
            admin_message = parts[1]
            
            # Ищем ID чата этого клиента в нашей базе данных
            if target_nick in client_database:
                client_chat_id = client_database[target_nick]
                try:
                    bot.send_message(client_chat_id, f"👑 **Сообщение от ИИ-Дизайнера:**\n\n{admin_message}")
                    bot.send_message(YOUR_TELEGRAM_CHAT_ID, f"✅ Ваш ответ успешно доставлен пользователю @{target_nick}!")
                except Exception as e:
                    bot.send_message(YOUR_TELEGRAM_CHAT_ID, f"❌ Не удалось отправить сообщение. Возможно, пользователь заблокировал бота.")
            else:
                bot.send_message(YOUR_TELEGRAM_CHAT_ID, f"❓ Ошибка! Пользователь `@{target_nick}` еще ни разу не запускал этого бота (не нажимал /start). Попросите его активировать бота, чтобы открыть канал связи!")
        else:
            bot.send_message(YOUR_TELEGRAM_CHAT_ID, "💡 **Инструкция для Шефа:**\n\nЧтобы написать клиенту, введите его ник и текст через пробел:\n`ivan_seller Привет, макет готов!`")
        return

    # --- РЕЖИМ КЛИЕНТА (Сбор входящих сообщений от селлеров для вас) ---
    if message.from_user.username:
        client_database[message.from_user.username.lower().strip()] = chat_id
        
    client_username = message.from_user.username or "Скрытый_Ник"
    
    # Пересылаем текст клиента вам в ЛС
    incoming_notification = f"💬 **Новое сообщение от клиента @{client_username}:**\n\n{text}\n\n" \
                            f"ℹ️ *Чтобы ответить ему, напишите в этот чат:* `{client_username} Ваш ответ`"
    bot.send_message(YOUR_TELEGRAM_CHAT_ID, incoming_notification)
    
    # Отвечаем клиенту заглушкой автоответчика студии
    bot.send_message(chat_id, "🤖 Ваш запрос зафиксирован и передан мастеру на проработку. Дизайнер ответит вам прямо в этом чате в течение нескольких минут!")

print("🚀 Обновленный Telegram-бот обратной связи успешно запущен...")
bot.infinity_polling()
