import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import io

# 1. إعدادات العرض الكامل
st.set_page_config(
    page_title="MUNTADHER Ultra Camera", 
    page_icon="📸", 
    layout="wide"
)

# كود CSS مكثف لإلغاء الهوامش وتوسيع الكاميرا
st.markdown("""
    <style>
    /* إخفاء الهوامش الجانبية والعلوية تماماً */
    .block-container {
        padding: 0rem !important;
        max-width: 100% !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* تكبير مساحة الكاميرا */
    .stCamera input {
        height: 400px !important;
    }
    div[data-testid="stImage"] img {
        width: 100% !important;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. العنوان
st.markdown("<h2 style='text-align: center; color: #00FFA2; background-color: #111; padding: 10px;'>📸 MUNTADHER CAMERA PRO</h2>", unsafe_allow_html=True)

# 3. استخدام الحاوية الكاملة
container = st.container()

with container:
    img_file = st.camera_input("التقط صورتك الآن")

    if img_file:
        original_img = Image.open(img_file)
        
        # وضع أدوات التحكم في صف واحد تحت الكاميرا لتوفير مساحة
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            base_filter = st.selectbox("الفلتر:", ["طبيعي", "أبيض وأسود", "سيبيا", "سلبي", "رسم"])
        with col_f2:
            blur_level = st.select_slider("التغبيش:", options=[0, 2, 5, 10])

        # محرك المعالجة
        processed_img = original_img
        if base_filter == "أبيض وأسود":
            processed_img = ImageOps.grayscale(processed_img)
        elif base_filter == "سيبيا":
            gray = ImageOps.grayscale(processed_img)
            processed_img = ImageOps.colorize(gray, "#704214", "#C0A080")
        elif base_filter == "سلبي":
            processed_img = ImageOps.invert(processed_img.convert("RGB"))
        elif base_filter == "رسم":
            processed_img = processed_img.filter(ImageFilter.CONTOUR)

        if blur_level > 0:
            processed_img = processed_img.filter(ImageFilter.GaussianBlur(radius=blur_level))

        # عرض النتيجة بملء العرض
        st.markdown("### 🖼️ النتيجة النهائية:")
        st.image(processed_img, use_container_width=True)
        
        # زر التحميل عريض جداً وسهل الضغط
        buf = io.BytesIO()
        processed_img.save(buf, format="PNG")
        st.download_button(
            label="📥 حفظ الصورة بملء الشاشة", 
            data=buf.getvalue(), 
            file_name="Muntadher_Pro.png", 
            mime="image/png",
            use_container_width=True
        )

st.markdown("<p style='text-align: center; color: #555; padding: 20px;'>MUNTADHER.H.ASD Engineering</p>", unsafe_allow_html=True)
