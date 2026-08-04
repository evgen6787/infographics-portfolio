import os
import sys
import subprocess

# СЕКРЕТНЫЙ ХАК: Принудительный запуск Telegram-бота на хостинге Streamlit
if "bot_started" not in os.environ:
    try:
        os.environ["bot_started"] = "true"
        # Запускаем bot.py в фоновом режиме, чтобы он не вешал работу самого сайта
        subprocess.Popen([sys.executable, "bot.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

import streamlit as st

# 1. Настройка вкладки браузера
st.set_page_config(
    page_title="Инфографика для маркетплейсов | InfographicsAI", 
    page_icon="🛍", 
    layout="centered"
)

# 2. Кастомные CSS-стили для тёмной темы и ВЕРИФИКАЦИЯ ЯНДЕКСА
st.markdown("""
    <!-- Специфический тег Яндекса, внедренный в верстку -->
    <meta name="yandex-verification" content="871b8699e77af33e" />
    
    <style>
    .stApp {
        background-color: #0D0D11 !important;
        color: #FFFFFF !important;
    }
    .promo-box {
        background-color: #1A1A24;
        border-left: 5px solid #00B4D8;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Умный поиск главного баннера в папке проекта
banner_file = None
for file in os.listdir("."):
    if "banner" in file.lower():
        banner_file = file
        break

# Выводим баннер или заголовок
if banner_file:
    st.image(banner_file, use_container_width=True)
else:
    st.title("🔥 Уникальная ИИ-инфографика для WB / Ozon")

st.write("""
Забудьте про унылые и заезженные бесплатные шаблоны, которые покупатели просто пролистывают. 
Я создаю уникальный визуальный контент с нуля с помощью нейросетей нового поколения (**Ideogram**, **FLUX**). 
ИИ генерирует сочный фон, сам товар и идеальный читаемый текст прямо на картинке!
""")

st.divider()

# 4. Блок Горящих Акций
st.header("🔥 Мега-Акции этой недели")
st.markdown("""
<div class="promo-box">
    <h3 style='color: #00B4D8; margin-top:0; font-size:18px;'>🎁 Акция "Быстрый Старт"</h3>
    <p style='margin:0;'>При заказе полной воронки от 5 слайдов — <b>Маркетинговый анализ 3 главных конкурентов</b> в вашей нише сделаю абсолютно БЕСПЛАТНО!</p>
</div>
<div class="promo-box">
    <h3 style='color: #7B2CBF; margin-top:0; font-size:18px;'>⚡️ Акция "Оптом Дешевле"</h3>
    <p style='margin:0;'>Заказываете инфографику сразу для 3 разных товаров? Получите фиксированную скидку <b>-15% на весь чек</b>!</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# 5. Визуальные плашки этапов сотрудничества
st.header("🛠 Как строится процесс работы?")
st.success("1️⃣ **Обсуждение ТЗ** — Вы присылаете фото товара и основные тезисы.")
st.info("2️⃣ **Предоплата** — Вносите 50% предоплаты для запуска API нейросети.")
st.warning("3️⃣ **Генерация и правки** — Смотрите готовые варианты с ватермаркой.")
st.error("4️⃣ **Получение оригинала** — Оплата оставшихся 50% и отправка файлов в 4K.")

st.divider()

# 6. Галерея портфолио
st.header("📂 Мои работы (Примеры)")
st.write("Нажмите на картинку, чтобы рассмотреть детали:")

col1, col2 = st.columns(2)
with col1:
    st.image("powerbank.jpg.png", caption="Повербанк в стиле Cyber Neon", use_container_width=True)
    st.image("cream.jpg.png", caption="Крем в стиле Эко-минимализм", use_container_width=True)
with col2:
    st.image("headphones.jpg.png", caption="Наушники в стиле Neon Hi-Tech", use_container_width=True)

st.divider()

# 7. Блок FAQ
st.header("💬 Частые вопросы")
with st.expander("Почему первая предоплата 50% не возвращается?"):
    st.write("Сумма предоплаты сразу же уходит на оплату API-ключей и мощностей серверов нейросетей коммерческого уровня (FLUX, Ideogram). Эти расходы списываются за каждую попытку генерации вашего товара, поэтому они являются фиксированными и невозвратными.")

with st.expander("Входят ли правки в стоимость?"):
    st.write("Все текстовые и графические правки в макете (изменить шрифт, подвинуть плашку, переписать фразу) выполняются абсолютно БЕСПЛАТНО до полного утверждения. Полная смена сгенерированной ИИ концепции фона по капризу заказчика оплачивается отдельно.")

st.divider()

# 8. Финальный призыв к действию
st.header("🤝 Как сделать заказ?")
st.info("💡 Ознакомьтесь с актуальной стоимостью во вкладке **«Цены и Акции»**, а затем перейдите во вкладку **«Сделать Заказ»** в меню слева. Наш умный чат-бот за 1 минуту поможет составить ТЗ и передаст заявку мне напрямую в Telegram!")
