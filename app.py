import gradio as gr
from transformers import pipeline

# تحميل نموذج ذكي ومجاني يعمل مباشرة على Hugging Face
generator = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-beta")

def chat_function(message, history):
    # تنسيق السؤال للنموذج
    prompt = f"User: {message}\nAssistant:"
    # توليد الرد (بدون الحاجة لـ API Key)
    results = generator(prompt, max_new_tokens=200, do_sample=True, temperature=0.7)
    response = results[0]['generated_text']
    return response.split("Assistant:")[-1].strip()

# واجهة المستخدم الاحترافية
demo = gr.ChatInterface(
    fn=chat_function, 
    title="🤖 مساعد MUNTADHER.ASD الذكي",
    theme="soft"
)

if __name__ == "__main__":
    demo.launch()
    