import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import io

# 1. إعدادات العرض الكامل (Full Width)
st.set_page_config(
    page_title="MUNTADHER Ultra Camera", 
    page_icon="📸", 
    layout="wide"
)

# 2. كود CSS مكثف لإلغاء الهوامش وجعل الكاميرا تملأ الشاشة
st.markdown("""
    <style>
    /* إلغاء الهوامش الجانبية والعلوية تماماً */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    /* إخفاء شعارات Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.stDeployButton {display: none !important;}
    
    /* تنسيق الكاميرا لتأخذ العرض الكامل */
    .stCamera {
        width: 100% !important;
    }
    div[data-testid="stImage"] img {
        width: 100% !important;
        height: auto;
        border-radius: 0px; /* جعل الحواف حادة لتملأ الشاشة */
    }
    /* تنسيق الأزرار لتكون كبيرة وسهلة اللمس */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #00FFA2;
        color: black;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة التطبيق
st.markdown("<h2 style='text-align: center; color: #00FFA2; background-color: #111; margin: 0; padding: 15px;'>📸 MUNTADHER CAMERA PRO</h2>", unsafe_allow_html=True)

# 4. محرك الكاميرا والمعالجة
# استخدمنا حاوية واحدة لضمان الترتيب الطولي المناسب للموبايل
main_container = st.container()

with main_container:
    # التقاط الصورة
    img_file = st.camera_input("التقط صورتك الآن")

    if img_file:
        original_img = Image.open(img_file)
        
        st.markdown("<h4 style='padding: 10px;'>🎨 لوحة التحكم بالفلاتر:</h4>", unsafe_allow_html=True)
        
        # توزيع أدوات التحكم في أعمدة صغيرة لتوفير المساحة
        col1, col2 = st.columns(2)
        with col1:
            base_filter = st.selectbox("الفلتر الأساسي:", 
                ["طبيعي", "أبيض وأسود", "سيبيا (قديم)", "سلبي (Negative)", "رسم زيتي"])
        with col2:
            blur_val = st.select_slider("قوة التغبيش:", options=[0, 2, 5, 10])

        # محرك الـ 100 فلتر (التحكم اليدوي)
        with st.expander("🛠️ تعديلات احترافية دقيقة (سطوع، ألوان، حدة)"):
            bright = st.slider("السطوع", 0.5, 2.0, 1.0)
            cont = st.slider("التباين", 0.5, 2.0, 1.0)
            saturation = st.slider("تشبع الألوان", 0.0, 3.0, 1.0)

        # تنفيذ المعالجة برمجياً
        processed_img = original_img
        
        # تطبيق القوالب
        if base_filter == "أبيض وأسود":
            processed_img = ImageOps.grayscale(processed_img)
        elif base_filter == "سيبيا (قديم)":
            gray = ImageOps.grayscale(processed_img)
            processed_img = ImageOps.colorize(gray, "#704214", "#C0A080")
        elif base_filter == "سلبي (Negative)":
            processed_img = ImageOps.invert(processed_img.convert("RGB"))
        elif base_filter == "رسم زيتي":
            processed_img = processed_img.filter(ImageFilter.CONTOUR)

        # تطبيق التعديلات الدقيقة
        processed_img = ImageEnhance.Brightness(processed_img).enhance(bright)
        processed_img = ImageEnhance.Contrast(processed_img).enhance(cont)
        processed_img = ImageEnhance.Color(processed_img).enhance(saturation)
        
        if blur_val > 0:
            processed_img = processed_img.filter(ImageFilter.GaussianBlur(radius=blur_val))

        # عرض النتيجة النهائية بملء العرض
        st.markdown("---")
        st.image(processed_img, use_container_width=True)
        
        # تحويل الصورة لبيانات للتحميل
        buf = io.BytesIO()
        processed_img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # زر التحميل بملء الشاشة
        st.download_button(
            label="📥 حفظ الصورة المعدلة بجودة HD",
            data=byte_im,
            file_name="Muntadher_Camera_Photo.png",
            mime="image/png",
            use_container_width=True
        )

# تذييل الصفحة
st.markdown("<p style='text-align: center; color: #555; padding: 20px;'>MUNTADHER.H.ASD Engineering © 2026</p>", unsafe_allow_html=True)
