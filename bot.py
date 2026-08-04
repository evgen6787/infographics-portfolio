import telebot
from telebot import types

# --- НАСТРОЙКА КЛЮЧЕЙ И ВАШЕГО ID ---
TELEGRAM_BOT_TOKEN = "8965640431:AAHVgQfVrj7HFHI2MYbCATAP4fMKwEIGsME"
YOUR_TELEGRAM_CHAT_ID = 1586057111
YOUR_TG_USERNAME = "dvaevgena"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Локальная база данных никнеймов селлеров
client_database = {}

# ГЛАВНОЕ ИНЛАЙН-МЕНЮ ДЛЯ КЛИЕНТОВ (Кнопки под сообщением)
def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📂 Смотреть примеры работ", callback_data="show_portfolio"),
        types.InlineKeyboardButton("📝 Условия и Сроки", callback_data="show_terms"),
        types.InlineKeyboardButton("🚦 Узнать статус моего заказа", callback_data="show_status"),
        types.InlineKeyboardButton("👑 Связаться с Дизайнером", callback_data="show_contact")
    )
    return markup

# ЭКСКЛЮЗИВНОЕ МЕНЮ ДЛЯ ВАС (Кнопки вместо клавиатуры внизу экрана)
def get_admin_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_list = types.KeyboardButton("📊 Список контактов базы")
    btn_promo = types.KeyboardButton("📢 Рассылка акции (-15%)")
    btn_help = types.KeyboardButton("💡 Справка по командам")
    markup.add(btn_list, btn_promo, btn_help)
    return markup

# 1. ОБРАБОТКА КОМАНДЫ /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    username = message.from_user.username
    
    if username:
        client_database[username.lower().strip()] = chat_id
        
    # Если запустил владелец студии
    if chat_id == YOUR_TELEGRAM_CHAT_ID or (username and username.lower() == YOUR_TG_USERNAME.lower()):
        bot.send_message(
            chat_id, 
            "👑 **Добро пожаловать, Шеф!**\n\nДля вас активирована скрытая панель управления. Используйте кнопки внизу экрана!",
            reply_markup=get_admin_keyboard(),
            parse_mode="Markdown"
        )
        return

    # Если запустил обычный клиент
    if username:
        bot.send_message(YOUR_TELEGRAM_CHAT_ID, f"🟢 Селлер @{username} (ID: {chat_id}) запустил бота!")
        
    welcome_text = "🎉 **Добро пожаловать в официальный бот студии InfographicsAI!**\n\n" \
                   "Я — ваш автоматический интерактивный помощник. Помогу сориентироваться по ценам и свяжу с мастером.\n\n" \
                   "👇 **Выберите интересующий вас раздел в меню ниже:**"
    bot.send_message(chat_id, welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")
# 2. ПРИЕМ ФОТОГРАФИЙ И МАТЕРИАЛОВ ОТ СЕЛЛЕРОВ
@bot.message_handler(content_types=['photo', 'document'])
def handle_docs_photos(message):
    chat_id = message.chat.id
    username = message.from_user.username or "Скрытый_Ник"
    
    if chat_id == YOUR_TELEGRAM_CHAT_ID:
        bot.send_message(YOUR_TELEGRAM_CHAT_ID, "💡 Чтобы ответить клиенту, введите: `ник_клиента Текст ответа`")
        return
        
    if message.from_user.username:
        client_database[message.from_user.username.lower().strip()] = chat_id

    bot.send_message(chat_id, "✅ **📸 Фотографии вашего товара успешно получены!**\n\nЯ мгновенно перенаправил их нашему дизайнеру. Мастер изучит ракурсы и качество картинок, после чего напишет вам прямо сюда!")
    bot.send_message(YOUR_TELEGRAM_CHAT_ID, f"🔔 **КЛИЕНТ ПРИСЛАЛ МАТЕРИАЛЫ!**\n👤 От: @{username}\nℹ Roy Напишите ему: `{username} Текст сообщения`")
    
    if message.content_type == 'photo':
        bot.send_photo(YOUR_TELEGRAM_CHAT_ID, message.photo[-1].file_id)
    else:
        bot.send_document(YOUR_TELEGRAM_CHAT_ID, message.document.file_id)

# 3. ОБРАБОТКА НАЖАТИЙ НА ИНЛАЙН-КНОПКИ КЛИЕНТАМИ
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬅️ Вернуться в меню", callback_data="back_to_menu"))
    
    if call.data == "show_portfolio":
        text = "📂 **Примеры наших лучших ИИ-генераций:**\n\n• Повербанк в стиле Cyber Neon 🔋\n• Наушники в стиле Hi-Tech Neon 🎧\n• Корейский крем в стиле Эко-минимализм 🌿\n\nВы можете рассмотреть эти макеты в 4K на нашем официальном сайте-витрине!"
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "show_terms":
        text = "📝 **Правила и Сроки работы студии:**\n\n1️⃣ **Сроки:** 1–3 рабочих дня на генерацию сочной карточки.\n2️⃣ **Предоплата:** Фиксированные 50% для запуска серверов нейросети (не возвращается).\n3️⃣ **Правки:** Изменение шрифтов, плашек и текста — бесплатно."
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "show_status":
        text = "🚦 **Статус вашего заказа:**\n\nЯ передал ваш запрос нашему дизайнеру! Прямо сейчас мастер настраивает свет и прорабатывает концепцию. Как только наброски первой обложки будут готовы, они прилетят вам сюда!"
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "show_contact":
        text = "👑 **Связь с Дизайнером:**\n\nВы можете задать любой сложный вопрос, обсудить оптовую скидку или прислать ТЗ напрямую.\n\n📸 **Просто пришлите фотографии вашего товара прямо в этот чат** (обычным фото или файлом) — и наш мастер мгновенно подключится к диалогу!"
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "back_to_menu":
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="👇 **Выберите интересующий вас раздел в меню ниже:**", reply_markup=get_main_menu(), parse_mode="Markdown")

# 4. ОБРАБОТКА ТЕКСТОВЫХ АДМИН-КНОПОК И СВЯЗИ
@bot.message_handler(func=lambda message: True)
def handle_admin_and_client_messages(message):
    chat_id = message.chat.id
    text = message.text.strip()
    username = message.from_user.username
    
    if username:
        client_database[username.lower().strip()] = chat_id

    # --- ЛОГИКА ДЛЯ ВАС (АДМИНИСТРАТОР @dvaevgena) ---
    if chat_id == YOUR_TELEGRAM_CHAT_ID or (username and username.lower() == YOUR_TG_USERNAME.lower()):
        
        # КНОПКА 1: Просмотр базы контактов
        if text == "📊 Список контактов базы":
            if client_database:
                db_text = "📊 **База активных клиентов студии:**\n\n"
                for nick, c_id in client_database.items():
                    db_text += f"🔹 @{nick} (ID: `{c_id}`)\n"
                bot.send_message(chat_id, db_text, parse_mode="Markdown")
            else:
                bot.send_message(chat_id, "ℹ️ База данных пуста. Клиенты еще не нажимали /start в этой сессии.")
                
        # КНОПКА 2: Массовая рассылка рекламы/акций
        elif text == "📢 Рассылка акции (-15%)":
            if client_database:
                promo_message = "🔥 **ВНИМАНИЕ, ГОРЯЩАЯ АКЦИЯ СТУДИИ!** 🔥\n\n" \
                                "Только в ближайшие 48 часов у нас действует скидка **-15% на весь чек** при заказе инфографики сразу для 3 разных товаров маркетплейсов!\n\n" \
                                "🤖 Чтобы зафиксировать за собой скидку, просто напишите нашему чат-боту название ваших товаров прямо сюда!"
                success_count = 0
                for nick, c_id in client_database.items():
                    try:
                        bot.send_message(c_id, promo_message, parse_mode="Markdown")
                        success_count += 1
                    except: pass
                bot.send_message(YOUR_TELEGRAM_CHAT_ID, f"📢 Рассылка завершена! Успешно доставлено {success_count} селлерам.")
            else:
                bot.send_message(chat_id, "❌ Некому отправлять рассылку, база пуста.")
                
        # КНОПКА 3: Быстрая справка по командам
        elif text == "💡 Справка по командам":
            help_text = "💡 **Как отвечать селлерам с сайта/бота:**\n\n" \
                        "Просто введите никнейм клиента без знака @ и ваш текст через один пробел:\n" \
                        "`ivan_seller Привет! Сделаем дизайн в лучшем виде, вот реквизиты на предоплату...`"
            bot.send_message(chat_id, help_text, parse_mode="Markdown")
            
        # Прямой ответ клиенту по его никнейму
        elif " " in text:
            parts = text.split(" ", 1)
            target_nick = parts[0].replace("@", "").lower().strip()
            admin_message = parts[1]
            
            if target_nick in client_database:
                try:
                    bot.send_message(client_database[target_nick], f"👑 **Сообщение от Дизайнера:**\n\n{admin_message}")
                    bot.send_message(YOUR_TELEGRAM_CHAT_ID, f"✅ Ответ успешно доставлен пользователю @{target_nick}!")
                except:
                    bot.send_message(YOUR_TELEGRAM_CHAT_ID, "❌ Ошибка! Пользователь заблокировал бота.")
            else:
                bot.send_message(YOUR_TELEGRAM_CHAT_ID, f"❓ Пользователь @{target_nick} еще не нажимал /start в боте. Нет канала связи!")
        else:
            bot.send_message(YOUR_TELEGRAM_CHAT_ID, "💡 Чтобы ответить клиенту, введите через пробел:\n`ник_клиента Текст ответа`")
        return

    # --- ЛОГИКА ДЛЯ ОБЫЧНЫХ ВХОДЯЩИХ КЛИЕНТОВ ---
    client_username = message.from_user.username or "Скрытый_Ник"
    incoming_notification = f"💬 **Новое сообщение от клиента @{client_username}:**\n\n{text}\n\n" \
                            f"ℹ️ *Ответить ему:* `{client_username} Ваш ответ`"
    bot.send_message(YOUR_TELEGRAM_CHAT_ID, incoming_notification)
    bot.send_message(chat_id, "🤖 Ваш запрос зафиксирован и передан мастеру! Дизайнер ответит вам прямо в этом чате в течение нескольких минут.")

print("🚀 Интерактивный Telegram-бот с админ-панелью успешно запущен...")
bot.infinity_polling()
