import os
import streamlit as st

# 1. Настройка вкладки браузера
st.set_page_config(
    page_title="Инфографика для маркетплейсов | InfographicsAI", 
    page_icon="🛍", 
    layout="centered"
)

# 2. Кастомные CSS-стили для тёмной темы и верификация Яндекса
st.markdown("""
    <!-- Специфический тег Яндекса, внедренный в верстку -->
    <meta name="yandex-verification" content="871b8699e77af33e" />
    
    <style>
    /* Глубокий космический фон */
    .stApp {
        background-color: #0A0A0E !important;
        color: #FFFFFF !important;
    }
    
    /* Сочные неоновые разделители вместо серых полос */
    hr {
        border: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #7B2CBF, #00B4D8, transparent);
        margin: 40px 0 !important;
    }
    
    /* Плашка акций */
    .promo-box {
        background: linear-gradient(135deg, #12121A, #1A1A26);
        border-left: 5px solid #00B4D8;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(0, 180, 216, 0.2);
    }
    
    /* Красивые карточки для этапов работы */
    .step-card {
        background: #14141F;
        border: 1px solid #24243A;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
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
    st.markdown("<h1 style='color: #00B4D8; text-shadow: 0 0 10px rgba(0,180,216,0.5);'>🔥 Уникальная ИИ-инфографика для WB / Ozon</h1>", unsafe_allow_html=True)

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
    <h3 style='color: #00B4D8; margin-top:0; font-size:18px; text-shadow: 0 0 10px rgba(0,180,216,0.3);'>🎁 Акция "Быстрый Старт"</h3>
    <p style='margin:0; opacity: 0.9;'>При заказе полной воронки от 5 слайдов — <b>Маркетинговый анализ 3 главных конкурентов</b> в вашей нише сделаю абсолютно БЕСПЛАТНО!</p>
</div>
<div class="promo-box">
    <h3 style='color: #7B2CBF; margin-top:0; font-size:18px; text-shadow: 0 0 10px rgba(123,44,191,0.3);'>⚡️ Акция "Оптом Дешевле"</h3>
    <p style='margin:0; opacity: 0.9;'>Заказываете инфографику сразу для 3 разных товаров? Получите фиксированную скидку <b>-15% на весь чек</b>!</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# 5. Визуальные плашки этапов сотрудничества в неоновом стиле
st.header("🛠 Как строится процесс работы?")
st.markdown("""
<div class="step-card" style="border-left: 4px solid #2ECC71;">
    <span style="color:#2ECC71; font-weight:bold;">1️⃣ Обсуждение ТЗ</span> — Вы присылаете фото товара и основные тезисы.
</div>
<div class="step-card" style="border-left: 4px solid #3498DB;">
    <span style="color:#3498DB; font-weight:bold;">2️⃣ Предоплата</span> — Вносите 50% предоплаты для запуска API нейросети.
</div>
<div class="step-card" style="border-left: 4px solid #F1C40F;">
    <span style="color:#F1C40F; font-weight:bold;">3️⃣ Генерация и правки</span> — Смотрите готовые варианты с ватермаркой.
</div>
<div class="step-card" style="border-left: 4px solid #E74C3C;">
    <span style="color:#E74C3C; font-weight:bold;">4️⃣ Получение оригинала</span> — Оплата оставшихся 50% и отправка файлов в 4K.
</div>
""", unsafe_allow_html=True)

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
