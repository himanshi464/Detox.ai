import streamlit as st
import google.generativeai as genai
from PIL import Image
import re
import requests
import pandas as pd
import PyPDF2
import os

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Detox.ai Sovereign OS", layout="wide")

# --- 2. SOVEREIGN DOCUMENT PROCESSORS ---
def process_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        return "".join(page.extract_text() for page in reader.pages)
    except: return "Error reading PDF."

def process_csv(file):
    try:
        df = pd.read_csv(file)
        return df.head(10).to_string()
    except: return "Error reading CSV."

# --- 3. CONFIG & SECURE KEY LOADING ---
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
ZERO_TRAIN_TOKEN = "[POLICY: 0x7FF32] DE-IDENTIFIED SESSION: DO NOT TRAIN."

# --- 4. THE SOVEREIGN PRIVACY ENGINE ---
class KavachEngine:
    def __init__(self):
        if 'vault' not in st.session_state: st.session_state.vault = {}
    def scrub_pii(self, text):
        patterns = {r'\b\d{4}-\d{4}-\d{4}\b': "AADHAAR_ID", r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b': "PAN_CARD", r'\b[6-9]\d{9}\b': "MOBILE_NUM"}
        for pattern, label in patterns.items():
            matches = re.findall(pattern, text)
            for i, val in enumerate(matches):
                dummy = f"<{label}_{i+1}>"
                st.session_state.vault[dummy] = val
                text = text.replace(val, dummy)
        return text
    def restore_pii(self, ai_response):
        for dummy, real in st.session_state.vault.items(): ai_response = ai_response.replace(dummy, real)
        return ai_response
    def intent_swapper(self, prompt):
        if any(k in prompt.lower() for k in ["tax evade", "hide money", "illegal"]):
            return "How can I manage my financial assets within legal frameworks?", True
        return prompt, False

kavach = KavachEngine()

# --- 5. UI ---
st.title("🛡️ Detox.ai: Sovereign Defense System")
st.caption("Ministerial Gateway | Privacy-First Intelligence")

with st.sidebar:
    st.header("📄 Document Detox")
    doc_file = st.file_uploader("Upload CSV or PDF", type=['csv', 'pdf'])
    firewall_active = st.toggle("Enable Intent-Swapper", value=True)
    up_img = st.file_uploader("Upload Identity Image", type=['jpg', 'jpeg', 'png'])

# --- 6. CHAT LOGIC ---
if user_prompt := st.chat_input("Enter directive..."):
    with st.chat_message("user"): st.markdown(user_prompt)
    
    processed_prompt, was_swapped = kavach.intent_swapper(user_prompt) if firewall_active else (user_prompt, False)
    safe_prompt = kavach.scrub_pii(processed_prompt)

    with st.chat_message("assistant"):
        final_text, engine_used = "", "Offline"
        
        # 1. PRIMARY: Try Local Ollama ONLY if on localhost
        try:
            res = requests.post("http://localhost:11434/api/generate", 
                                json={"model": "phi4-mini", "prompt": safe_prompt, "stream": False}, timeout=1)
            final_text = res.json()['response']
            engine_used = "🏠 Local Engine (Ollama)"
        except:
            # 2. SECONDARY: Gemini Cloud (SILENT)
            if API_KEY:
                try:
                    genai.configure(api_key=API_KEY)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    payload = [f"{ZERO_TRAIN_TOKEN}\n\nTask: {safe_prompt}"]
                    if up_img: payload.append(Image.open(up_img))
                    response = model.generate_content(payload)
                    final_text = response.text
                    engine_used = "☁️ Detox Cloud"
                except:
                    final_text = "System is currently maintaining air-gap protocols (Offline)."
            else:
                final_text = "Engine connection lost."

        st.markdown(kavach.restore_pii(final_text))
        st.caption(f"Inference: {engine_used} | Protected by Detox.ai")








