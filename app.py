import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import io

# 1. تفعيل وضع العرض الكامل (layout="wide")
st.set_page_config(
    page_title="MUNTADHER Ultra Camera", 
    page_icon="📸", 
    layout="wide"  # هذا هو السر في جعل التطبيق يملأ الشاشة
)

# إخفاء العلامات المائية تماماً
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.stDeployButton {display: none !important;}
    /* تقليل الهوامش العلوية والسفلية */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. العنوان بملئ الشاشة
st.markdown("<h1 style='text-align: center; color: #00FFA2; font-size: 3rem;'>📸 MUNTADHER Ultra Camera</h1>", unsafe_allow_html=True)
st.write("---")

# 3. استخدام الحاويات بملئ الشاشة
# جعلنا النسبة 1:1 أو 2:1 لتعطيك مساحة أكبر للعرض
col_ctrl, col_view = st.columns([1, 2])

with col_ctrl:
    st.markdown("### 🛠️ المختبر")
    img_file = st.camera_input("افتح الكاميرا")
    
    if img_file:
        st.write("---")
        base_filter = st.selectbox("القالب الأساسي:", 
            ["طبيعي", "أبيض وأسود", "سيبيا (قديم)", "سلبي (Negative)", "رسم زيتي"])
        
        brightness = st.slider("السطوع", 0.0, 3.0, 1.0)
        contrast = st.slider("التباين", 0.0, 3.0, 1.0)
        color = st.slider("الألوان", 0.0, 5.0, 1.0)
        blur_level = st.slider("التغبيش", 0, 10, 0)

with col_view:
    if img_file:
        original_img = Image.open(img_file)
        
        # معالجة الصورة
        processed_img = original_img
        if base_filter == "أبيض وأسود":
            processed_img = ImageOps.grayscale(processed_img)
        elif base_filter == "سيبيا (قديم)":
            gray = ImageOps.grayscale(processed_img)
            processed_img = ImageOps.colorize(gray, "#704214", "#C0A080")
        elif base_filter == "سلبي (Negative)":
            processed_img = ImageOps.invert(processed_img.convert("RGB"))
        elif base_filter == "رسم زيتي":
            processed_img = processed_img.filter(ImageFilter.CONTOUR)

        # التعديلات الدقيقة
        processed_img = ImageEnhance.Brightness(processed_img).enhance(brightness)
        processed_img = ImageEnhance.Contrast(processed_img).enhance(contrast)
        processed_img = ImageEnhance.Color(processed_img).enhance(color)
        if blur_level > 0:
            processed_img = processed_img.filter(ImageFilter.GaussianBlur(radius=blur_level))

        # عرض الصورة بملئ مساحة العمود
        st.image(processed_img, use_container_width=True)
        
        # زر التحميل بشكل عريض
        buf = io.BytesIO()
        processed_img.save(buf, format="PNG")
        st.download_button(
            label="📥 حفظ الصورة النهائية", 
            data=buf.getvalue(), 
            file_name="Muntadher_Full_HD.png", 
            mime="image/png",
            use_container_width=True
        )
    else:
        # رسالة تظهر قبل التقاط الصورة تشغل مساحة الشاشة
        st.info("قم بفتح الكاميرا والتقاط صورة لتبدأ المعالجة بملئ الشاشة.")

st.markdown("<p style='text-align: center; color: #555; margin-top: 50px;'>MUNTADHER.H.ASD Engineering</p>", unsafe_allow_html=True)
