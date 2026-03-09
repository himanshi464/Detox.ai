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
    reader = PyPDF2.PdfReader(file)
    text = "".join(page.extract_text() for page in reader.pages)
    return text

def process_csv(file):
    df = pd.read_csv(file)
    return df.head(10).to_string()

# --- 3. CONFIG & SECURE KEY LOADING ---
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

ZERO_TRAIN_TOKEN = """
[POLICY_ENFORCEMENT: 0x7FF32]
DE-IDENTIFIED SESSION: DO NOT LOG. DO NOT TRAIN.
"""

# --- 4. THE SOVEREIGN PRIVACY ENGINE ---
class KavachEngine:
    def __init__(self):
        if 'vault' not in st.session_state:
            st.session_state.vault = {}

    def scrub_pii(self, text):
        patterns = {
            r'\b\d{4}-\d{4}-\d{4}\b': "AADHAAR_ID",
            r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b': "PAN_CARD",
            r'\b[6-9]\d{9}\b': "MOBILE_NUM"
        }
        for pattern, label in patterns.items():
            matches = re.findall(pattern, text)
            for i, val in enumerate(matches):
                dummy = f"<{label}_{i+1}>"
                st.session_state.vault[dummy] = val
                text = text.replace(val, dummy)
        return text

    def restore_pii(self, ai_response):
        for dummy, real in st.session_state.vault.items():
            ai_response = ai_response.replace(dummy, real)
        return ai_response

    def intent_swapper(self, prompt):
        risky_keywords = ["tax evade", "hide money", "illegal", "bypass"]
        if any(k in prompt.lower() for k in risky_keywords):
            return "How can I manage my financial assets within legal frameworks securely?", True
        return prompt, False

kavach = KavachEngine()

# --- 5. THE UI & SIDEBAR ---
st.title("🛡️ Detox.ai: Sovereign Defense System")
st.caption("Ministerial Gateway | Privacy-First Intelligence")

with st.sidebar:
    st.header("📄 Document Detox")
    doc_file = st.file_uploader("Upload CSV or PDF for Summary", type=['csv', 'pdf'])
    
    st.divider()
    st.header("🌐 Memetic Firewall")
    firewall_active = st.toggle("Enable Intent-Swapper", value=True)
    
    st.divider()
    st.header("📤 Vision AI")
    up_img = st.file_uploader("Upload Identity Image", type=['jpg', 'jpeg', 'png'])

# --- 6. MAIN LOGIC: DOCUMENT SUMMARIZATION ---
if doc_file and st.button("Summarize Uploaded Document"):
    with st.chat_message("assistant"):
        raw_text = process_pdf(doc_file) if doc_file.type == "application/pdf" else process_csv(doc_file)
        safe_doc_text = kavach.scrub_pii(raw_text[:4000])
        summary_prompt = f"Provide a concise summary of this data: {safe_doc_text}"
        
        final_summary, engine = "", "Checking..."

        # PRIMARY: Local Ollama
        try:
            res = requests.post("http://localhost:11434/api/generate", 
                                json={"model": "phi4-mini", "prompt": summary_prompt, "stream": False}, timeout=5)
            final_summary = res.json()['response']
            engine = "🏠 Local Engine (Ollama)"
        except:
            # SILENT SECONDARY: Cloud Fallback
            if API_KEY:
                try:
                    genai.configure(api_key=API_KEY)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content([f"{ZERO_TRAIN_TOKEN}\n{summary_prompt}"])
                    final_summary = response.text
                    engine = "☁️ Detox Cloud (Fallback)"
                except:
                    final_summary, engine = "❌ Local engine offline & Cloud fallback failed.", "Error"
            else:
                final_summary, engine = "❌ Local engine offline.", "Offline"
        
        st.write(kavach.restore_pii(final_summary))
        st.caption(f"Engine: {engine}")

# --- 7. MAIN LOGIC: CHAT & AUTO-FAILOVER ---
if user_prompt := st.chat_input("Enter directive..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)

    final_text, engine_used, was_swapped = "", "Awaiting Local...", False
    processed_prompt, was_swapped = kavach.intent_swapper(user_prompt) if firewall_active else (user_prompt, False)
    safe_prompt = kavach.scrub_pii(processed_prompt)

    with st.chat_message("assistant"):
        # 1. PRIMARY: OLLAMA (Local)
        try:
            res = requests.post("http://localhost:11434/api/generate", 
                                json={"model": "phi4-mini", "prompt": safe_prompt, "stream": False}, 
                                timeout=5)
            final_text = res.json()['response']
            engine_used = "🏠 Local Engine (Ollama)"
        except Exception:
            # 2. SILENT SECONDARY: GEMINI (Fallback)
            if API_KEY:
                try:
                    genai.configure(api_key=API_KEY)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    payload = [f"{ZERO_TRAIN_TOKEN}\n\nTask: {safe_prompt}"]
                    if up_img:
                        payload.append(Image.open(up_img))
                    
                    response = model.generate_content(payload)
                    final_text = response.text
                    engine_used = "☁️ Detox Cloud (Fallback)"
                except Exception:
                    final_text = "Service is currently unavailable locally and via cloud."
                    engine_used = "Unavailable"
            else:
                final_text = "Local engine is currently offline."
                engine_used = "Offline"

        st.markdown(kavach.restore_pii(final_text))
        st.caption(f"Engine: {engine_used} | Protected by Detox.ai")

    with st.expander("🔍 Sovereign Logs"):
        st.warning(f"What the AI saw: {safe_prompt}")
        if was_swapped:
            st.error("⚠️ Intent Neutralized by Firewall")







