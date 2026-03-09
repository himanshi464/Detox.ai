import streamlit as st
import google.generativeai as genai
from PIL import Image
import re
import random
import requests
import io
import pandas as pd
import PyPDF2
import os

# --- 1. PAGE CONFIG (Must be the very first Streamlit command) ---
st.set_page_config(page_title="Detox.ai Sovereign OS", layout="wide")

# --- 2. SOVEREIGN DOCUMENT PROCESSORS ---
def process_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def process_csv(file):
    df = pd.read_csv(file)
    return df.head(10).to_string()

# --- 3. CONFIG & SECURE KEY LOADING ---
# Silent loading to avoid red error boxes at the top
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
        
        # Local-First attempt for speed
        try:
            res = requests.post("http://localhost:11434/api/generate", 
                                json={"model": "phi4-mini", "prompt": summary_prompt, "stream": False}, timeout=2)
            final_summary = res.json()['response']
            engine = "🏠 Local Engine (Ollama)"
        except:
            if API_KEY:
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([f"{ZERO_TRAIN_TOKEN}\n{summary_prompt}"])
                final_summary = response.text
                engine = "☁️ Detox Cloud"
            else:
                final_summary = "❌ No engine available."
        
        st.write(kavach.restore_pii(final_summary))
        st.caption(f"Engine: {engine}")

# --- 6. MAIN LOGIC: CHAT & AUTO-FAILOVER ---
if user_prompt := st.chat_input("Enter directive..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Initialize variables to avoid NameError
    final_text = ""
    engine_used = "None"
    was_swapped = False

    processed_prompt, was_swapped = kavach.intent_swapper(user_prompt) if firewall_active else (user_prompt, False)
    safe_prompt = kavach.scrub_pii(processed_prompt)

    with st.chat_message("assistant"):
        # 1. TRY LOCAL FIRST (Ollama)
        try:
            res = requests.post("http://localhost:11434/api/generate", 
                                json={"model": "phi4-mini", "prompt": safe_prompt, "stream": False}, 
                                timeout=2)
            final_text = res.json()['response']
            engine_used = "🏠 Local Engine (Ollama)"
        except Exception:
            # 2. FALLBACK TO CLOUD (Gemini)
            if API_KEY:
                try:
                    genai.configure(api_key=API_KEY)
                    # Correct model name for 2026 is 'gemini-1.5-flash'
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    payload = [f"{ZERO_TRAIN_TOKEN}\n\nTask: {safe_prompt}"]
                    if up_img:
                        payload.append(Image.open(up_img))
                    
                    response = model.generate_content(payload)
                    final_text = response.text
                    engine_used = "☁️ Detox Cloud (Gemini)"
                except Exception as e:
                    final_text = f"❌ Cloud Error: {str(e)}"
                    engine_used = "Error"
            else:
                final_text = "❌ No API Key found and Local Engine is offline."
                engine_used = "Offline"

        # Display results
        st.markdown(kavach.restore_pii(final_text))
        st.caption(f"Engine: {engine_used} | Protected by Detox.ai")

    # --- 7. LIVE LOGS ---
    with st.expander("🔍 Sovereign Logs"):
        st.warning(f"What the AI saw: {safe_prompt}")
        if was_swapped:
            st.error("⚠️ Intent Neutralized by Firewall")




