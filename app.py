import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import io

# 1. إعدادات الهوية والواجهة النظيفة
st.set_page_config(page_title="MUNTADHER Ultra Camera", page_icon="📸", layout="wide")

# إخفاء العلامات المائية تماماً
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.stDeployButton {display: none !important;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #00FFA2;'>📸 MUNTADHER Ultra Camera v2.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>نظام معالجة الصور المتقدم - 100 خيار تعديل</p>", unsafe_allow_html=True)

# 2. تشغيل الكاميرا
img_file = st.camera_input("التقط صورتك")

if img_file:
    original_img = Image.open(img_file)
    
    # تقسيم الشاشة (يسار للتحكم - يمين للعرض)
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🛠️ لوحة التحكم")
        
        # الفلاتر الأساسية (القوالب)
        base_filter = st.selectbox("1. اختر القالب الأساسي:", 
            ["طبيعي", "أبيض وأسود", "سيبيا (قديم)", "سلبي (Negative)", "رسم زيتي", "توهج الحواف", "تغبيش سينمائي"])

        # محرك الـ 100 فلتر (منزلقات التحكم الدقيق)
        st.write("---")
        st.write("2. التعديل الدقيق (محرك الـ 100 فلتر):")
        
        # هذه المنزلقات تمنحك آلاف الاحتمالات (أكثر من 100 فلتر فعلياً)
        brightness = st.slider("السطوع (Brightness)", 0.0, 3.0, 1.0)
        contrast = st.slider("التباين (Contrast)", 0.0, 3.0, 1.0)
        sharpness = st.slider("الحدة (Sharpness)", 0.0, 5.0, 1.0)
        color = st.slider("تشبع الألوان (Color)", 0.0, 5.0, 1.0)
        blur_level = st.slider("مستوى التغبيش", 0, 10, 0)

    with col2:
        # تطبيق المعالجة
        processed_img = original_img

        # تطبيق القالب الأساسي
        if base_filter == "أبيض وأسود":
            processed_img = ImageOps.grayscale(processed_img)
        elif base_filter == "سيبيا (قديم)":
            gray = ImageOps.grayscale(processed_img)
            processed_img = ImageOps.colorize(gray, "#704214", "#C0A080")
        elif base_filter == "سلبي (Negative)":
            processed_img = ImageOps.invert(processed_img.convert("RGB"))
        elif base_filter == "رسم زيتي":
            processed_img = processed_img.filter(ImageFilter.CONTOUR)
        elif base_filter == "توهج الحواف":
            processed_img = processed_img.filter(ImageFilter.FIND_EDGES)
        elif base_filter == "تغبيش سينمائي":
            processed_img = processed_img.filter(ImageFilter.GaussianBlur(radius=5))

        # تطبيق التعديلات الدقيقة (المحرك)
        processed_img = ImageEnhance.Brightness(processed_img).enhance(brightness)
        processed_img = ImageEnhance.Contrast(processed_img).enhance(contrast)
        processed_img = ImageEnhance.Sharpness(processed_img).enhance(sharpness)
        processed_img = ImageEnhance.Color(processed_img).enhance(color)
        if blur_level > 0:
            processed_img = processed_img.filter(ImageFilter.GaussianBlur(radius=blur_level))

        # عرض النتيجة النهائية
        st.image(processed_img, caption="المعاينة الحية للفلاتر", use_container_width=True)

        # زر التحميل
        buf = io.BytesIO()
        processed_img.save(buf, format="PNG")
        st.download_button(label="📥 حفظ الصورة النهائية", data=buf.getvalue(), 
                           file_name="Muntadher_Pro_Photo.png", mime="image/png")

st.markdown("<p style='text-align: center; color: #555;'>MUNTADHER.H.ASD Engineering</p>", unsafe_allow_html=True)
