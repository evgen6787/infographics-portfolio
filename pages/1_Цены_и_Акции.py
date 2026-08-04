import os
import streamlit as st

st.set_page_config(page_title="Цены и Акции | InfographicsAI", page_icon="💰", layout="centered")

# Фирменный стиль для кнопок и плашек акций
st.markdown("""
    <style>
    div.stLinkButton > a {
        background: linear-gradient(135deg, #7B2CBF, #00B4D8) !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 0 15px rgba(123, 44, 191, 0.6) !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 12px 24px !important;
        text-decoration: none !important;
    }
    div.stLinkButton > a:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 0 25px rgba(0, 180, 216, 0.9) !important;
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

# Умный поиск баннера для бокового меню
banner_file = None
for file in os.listdir("."):
    if "banner" in file.lower():
        banner_file = file
        break

# --- ОФОРМЛЕНИЕ БОКОВОГО МЕНЮ (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00B4D8;'>🔥 InfographicsAI</h2>", unsafe_allow_html=True)
    if banner_file:
        st.image(banner_file, use_container_width=True)
    st.markdown("""
    <div style='text-align: center; font-size: 14px; color: #888888; margin-bottom: 20px;'>
        <b>ИИ-Дизайнер инфографики</b><br>
        Создаю визуал, который продает!
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("📌 **Навигация по сайту:**")

# --- ГЛАВНЫЙ КОНТЕНТ СТРАНИЦЫ ---
st.title("💰 Прайс-лист и Горящие Акции")
st.write("Выберите подходящий формат генерации для вашего бизнеса на маркетплейсах.")

st.divider()

# БЛОК 1: ГОРЯЩИЕ АКЦИИ
st.header("🔥 Мега-Акции этой недели")

st.markdown("""
<div class="promo-box">
    <h3 style='color: #00B4D8; margin-top:0;'>🎁 Акция "Быстрый Старт"</h3>
    <p>При заказе полной воронки от 5 слайдов — <b>Маркетинговый анализ 3 главных конкурентов</b> в вашей нише сделаю абсолютно БЕСПЛАТНО!</p>
</div>
<div class="promo-box">
    <h3 style='color: #7B2CBF; margin-top:0;'>⚡️ Акция "Оптом Дешевле"</h3>
    <p>Заказываете инфографику сразу для 3 разных товаров? Получите фиксированную скидку <b>-15% на весь чек</b>!</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# БЛОК 2: ТАРИФЫ
st.header("💎 Наши Тарифы")

tab1, tab2, tab3 = st.tabs([
    "🚀 Тест Ниши (1 слайд)", 
    "👑 Премиум-Воронка", 
    "🎭 Сложный (с Моделями)"
])

with tab1:
    st.markdown("### **300 руб. / слайд**")
    st.markdown("**Для кого:** Для быстрого старта, теста новых товаров на WB/Ozon или штучных заказов.")
    st.write("• Полная генерация ИИ под ключ: интеграция предмета в сочный неоновый, эко или мраморный фон.")
    st.write("• Выделение ключевых преимуществ товара, проработка ровного русского текста и инфо-плашек.")
    st.write("• Сроки выполнения: **1–2 дня**.")

with tab2:
    st.markdown("### **от 250 руб. / слайд (при заказе от 5 шт.)**")
    st.markdown("**Для кого:** Для селлеров, готовых выжимать максимум продаж со всей карточки товара.")
    st.write("• Разработка сквозной логики и воронки: Главная обложка -> Характеристики в цифрах -> Комплектация -> CTA.")
    st.write("• Глубокая проработка болей и триггеров вашей целевой аудитории через ИИ.")
    st.write("• Сроки выполнения: **2–3 дня**.")

with tab3:
    st.markdown("### **от 700 руб. / слайд**")
    st.markdown("**Для кого:** Одежда, обувь, товары для красоты, бьюти-сфера и премиум-аксессуары.")
    st.write("• Высокотехнологичная генерация фотореалистичных ИИ-моделей (людей) в движении.")
    st.write("• Демонстрация товара в реальной жизни (одежда на человеке, крем на лице, гаджет в руках).")
    st.write("• Сроки выполнения: **2–4 дня**.")

st.divider()

# Блок действия
st.header("🤝 Готовы запустить продажи?")
st.write("В моем Telegram-канале вы найдете всю подробную информацию по заказу: актуальный прайс-лист, пошаговые этапы работы и условия невозвратной предоплаты!")

st.link_button("👉 ПЕРЕЙТИ В TELEGRAM-КАНАЛ 👈", "https://t.me")
