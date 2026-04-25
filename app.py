import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import io

# 1. إعدادات العرض الكامل (Layout Wide)
st.set_page_config(page_title="MUNTADHER SNAP", layout="wide")

# 2. كود CSS "سناب شات" لإخفاء كل شيء وجعل الكاميرا هي الأساس
st.markdown("""
    <style>
    /* إخفاء الهوامش والعناصر الافتراضية */
    .block-container { padding: 0rem !important; max-width: 100% !important; }
    #MainMenu, footer, header { visibility: hidden; }
    div.stDeployButton { display: none !important; }
    
    /* خلفية سوداء كاملة مثل السناب */
    stApp { background-color: black; }
    
    /* تنسيق الكاميرا لتملأ الشاشة طوليًا */
    .stCamera { width: 100% !important; }
    .stCamera video { border-radius: 0px; object-fit: cover; height: 70vh !important; }
    
    /* تنسيق الأزرار لتكون دائرية واحترافية */
    .stButton>button {
        border-radius: 50px !important;
        height: 60px !important;
        width: 100% !important;
        background-color: #FFFC00 !important; /* لون سناب شات الأصفر */
        color: black !important;
        font-weight: bold !important;
        border: none !important;
    }
    
    /* شريط الفلاتر السفلي */
    .filter-bar {
        background: rgba(0,0,0,0.5);
        padding: 10px;
        border-radius: 20px;
        margin: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة السناب
st.markdown("<h3 style='text-align: center; color: white; padding: 10px;'>📸 MUNTADHER SNAP</h3>", unsafe_allow_html=True)

# استخدام حاوية الكاميرا
img_file = st.camera_input("") # ترك العنوان فارغاً لشبه السناب

if img_file:
    original_img = Image.open(img_file)
    
    # قائمة فلاتر بأسلوب سناب (أزرار أفقية)
    st.markdown("<p style='text-align: center; color: #FFFC00;'>اختر فلتر السناب الخاص بك:</p>", unsafe_allow_html=True)
    
    # استخدام أعمدة صغيرة تشبه شريط الفلاتر
    col1, col2, col3 = st.columns(3)
    with col1:
        f_type = st.selectbox("الفلتر", ["عادي", "أبيض وأسود", "سيبيا", "رسم", "توهج"])
    with col2:
        bright = st.slider("إضاءة", 0.5, 2.0, 1.0)
    with col3:
        smooth = st.slider("نعومة", 0, 10, 0)

    # معالجة الصورة
    proc_img = original_img
    if f_type == "أبيض وأسود": proc_img = ImageOps.grayscale(proc_img)
    elif f_type == "سيبيا": 
        proc_img = ImageOps.colorize(ImageOps.grayscale(proc_img), "#704214", "#C0A080")
    elif f_type == "رسم": proc_img = proc_img.filter(ImageFilter.CONTOUR)
    elif f_type == "توهج": proc_img = proc_img.filter(ImageFilter.EDGE_ENHANCE)

    # تطبيق السطوع والنعومة
    proc_img = ImageEnhance.Brightness(proc_img).enhance(bright)
    if smooth > 0: proc_img = proc_img.filter(ImageFilter.GaussianBlur(radius=smooth))

    # عرض النتيجة بملء الشاشة
    st.image(proc_img, use_container_width=True)

    # زر الحفظ (بستايل سناب شات)
    buf = io.BytesIO()
    proc_img.save(buf, format="PNG")
    st.download_button(
        label="💾 حفظ في الاستوديو",
        data=buf.getvalue(),
        file_name="Snap_Muntadher.png",
        mime="image/png"
    )

else:
    # واجهة تظهر قبل التصوير تشبه شاشة السناب السوداء
    st.markdown("""
        <div style='height: 300px; display: flex; align-items: center; justify-content: center;'>
            <p style='color: #555;'>جاهز لالتقاط اللقطة؟</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #333; font-size: 10px;'>MUNTADHER.H.ASD Engineering</p>", unsafe_allow_html=True)

