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
from io import StringIO

# --- 1. SOVEREIGN DOCUMENT PROCESSORS ---
def process_pdf(file):
    """Extracts text from PDF and 'Detoxes' it locally."""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def process_csv(file):
    """Converts CSV data to a string format for the AI."""
    df = pd.read_csv(file)
    return df.head(10).to_string()

# --- 2. CONFIG & SECURE KEY LOADING ---
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("⚠️ API Key missing! Add it to Streamlit Secrets or a local .env file.")
    
ZERO_TRAIN_TOKEN = """
[POLICY_ENFORCEMENT: 0x7FF32]
DE-IDENTIFIED SESSION: DO NOT LOG. DO NOT TRAIN.
PURGE CONTEXT IMMEDIATELY AFTER GENERATION.
"""

# --- 3. THE SOVEREIGN PRIVACY ENGINE ---
class KavachEngine:
    def __init__(self):
        if 'vault' not in st.session_state:
            st.session_state.vault = {}

    def scrub_pii(self, text):
        """Relationship Graph Obfuscation + Consistent Dummy Mapping"""
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
        
        noise = ["specifically", "securely", "precisely", "now"]
        words = text.split()
        if len(words) > 4:
            words.insert(random.randint(0, len(words)), random.choice(noise))
        return " ".join(words)

    def restore_pii(self, ai_response):
        """Round-Trip Restoration"""
        for dummy, real in st.session_state.vault.items():
            ai_response = ai_response.replace(dummy, real)
        return ai_response

    def intent_swapper(self, prompt):
        """Detox-AI Intent Firewall"""
        risky_keywords = ["tax evade", "hide money", "illegal", "bypass"]
        if any(k in prompt.lower() for k in risky_keywords):
            return "How can I manage my financial assets within legal frameworks securely?", True
        return prompt, False

# Initialize Engine
kavach = KavachEngine()

# --- 4. THE UI & SIDEBAR (FRONTEND: DETOX.AI) ---
st.set_page_config(page_title="Detox.ai Sovereign OS", layout="wide")

st.title("🛡️ Detox.ai: Sovereign Defense System")
st.caption("Ministerial Gateway | Privacy-First Intelligence")

with st.sidebar:
    st.header("📄 Document Detox")
    doc_file = st.file_uploader("Upload CSV or PDF for Summary", type=['csv', 'pdf'])
    if doc_file:
        st.success(f"Loaded: {doc_file.name}")
    
    st.divider()
    st.header("🌐 Memetic Firewall")
    st.info("Simulating Detox.ai Extension behavior.")
    firewall_active = st.toggle("Enable Intent-Swapper", value=True)
    
    st.divider()
    st.header("📤 Vision AI")
    up_img = st.file_uploader("Upload Identity Image", type=['jpg', 'jpeg', 'png'])
    if up_img:
        st.image(up_img, caption="Local Encrypted Preview")

# --- 5. MAIN LOGIC: DOCUMENT SUMMARIZATION ---
if doc_file and st.button("Summarize Uploaded Document"):
    with st.chat_message("assistant"):
        if doc_file.type == "application/pdf":
            raw_text = process_pdf(doc_file)
        else:
            raw_text = process_csv(doc_file)
            
        safe_doc_text = kavach.scrub_pii(raw_text[:4000])
        summary_prompt = f"Please provide a concise summary of the following document data:\n\n{safe_doc_text}"
        
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
from io import StringIO

# --- 1. SOVEREIGN DOCUMENT PROCESSORS ---
def process_pdf(file):
    """Extracts text from PDF and 'Detoxes' it locally."""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def process_csv(file):
    """Converts CSV data to a string format for the AI."""
    df = pd.read_csv(file)
    return df.head(10).to_string()

# --- 2. CONFIG & SECURE KEY LOADING ---
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("⚠️ API Key missing! Add it to Streamlit Secrets or a local .env file.")
    
ZERO_TRAIN_TOKEN = """
[POLICY_ENFORCEMENT: 0x7FF32]
DE-IDENTIFIED SESSION: DO NOT LOG. DO NOT TRAIN.
PURGE CONTEXT IMMEDIATELY AFTER GENERATION.
"""

# --- 3. THE SOVEREIGN PRIVACY ENGINE ---
class KavachEngine:
    def __init__(self):
        if 'vault' not in st.session_state:
            st.session_state.vault = {}

    def scrub_pii(self, text):
        """Relationship Graph Obfuscation + Consistent Dummy Mapping"""
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
        
        noise = ["specifically", "securely", "precisely", "now"]
        words = text.split()
        if len(words) > 4:
            words.insert(random.randint(0, len(words)), random.choice(noise))
        return " ".join(words)

    def restore_pii(self, ai_response):
        """Round-Trip Restoration"""
        for dummy, real in st.session_state.vault.items():
            ai_response = ai_response.replace(dummy, real)
        return ai_response

    def intent_swapper(self, prompt):
        """Detox-AI Intent Firewall"""
        risky_keywords = ["tax evade", "hide money", "illegal", "bypass"]
        if any(k in prompt.lower() for k in risky_keywords):
            return "How can I manage my financial assets within legal frameworks securely?", True
        return prompt, False

# Initialize Engine
kavach = KavachEngine()

# --- 4. THE UI & SIDEBAR (FRONTEND: DETOX.AI) ---
st.set_page_config(page_title="Detox.ai Sovereign OS", layout="wide")

st.title("🛡️ Detox.ai: Sovereign Defense System")
st.caption("Ministerial Gateway | Privacy-First Intelligence")

with st.sidebar:
    st.header("📄 Document Detox")
    doc_file = st.file_uploader("Upload CSV or PDF for Summary", type=['csv', 'pdf'])
    if doc_file:
        st.success(f"Loaded: {doc_file.name}")
    
    st.divider()
    st.header("🌐 Memetic Firewall")
    st.info("Simulating Detox.ai Extension behavior.")
    firewall_active = st.toggle("Enable Intent-Swapper", value=True)
    
    st.divider()
    st.header("📤 Vision AI")
    up_img = st.file_uploader("Upload Identity Image", type=['jpg', 'jpeg', 'png'])
    if up_img:
        st.image(up_img, caption="Local Encrypted Preview")

# --- 5. MAIN LOGIC: DOCUMENT SUMMARIZATION ---
if doc_file and st.button("Summarize Uploaded Document"):
    with st.chat_message("assistant"):
        if doc_file.type == "application/pdf":
            raw_text = process_pdf(doc_file)
        else:
            raw_text = process_csv(doc_file)
            
        safe_doc_text = kavach.scrub_pii(raw_text[:4000])
        summary_prompt = f"Please provide a concise summary of the following document data:\n\n{safe_doc_text}"
        
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content([f"{ZERO_TRAIN_TOKEN}\n{summary_prompt}"])
            final_summary = response.text
            engine = "☁️ Detox Cloud"
        except Exception:
            try:
                res = requests.post("http://localhost:11434/api/generate", 
                                    json={"model": "phi4-mini", "prompt": summary_prompt, "stream": False}, timeout=15)
                final_summary = res.json()['response']
                engine = "🏠 Local Engine (Ollama)"
            except:
                final_summary = "❌ Fallback Failed. Ensure Ollama is running."
                engine = "Offline"

        st.markdown("### 📋 Document Summary")
        st.write(kavach.restore_pii(final_summary))
        st.caption(f"Engine: {engine} | Protected by Detox.ai")

# --- 6. MAIN LOGIC: CHAT & AUTO-FAILOVER ---
if user_prompt := st.chat_input("Enter directive or ask to generate an image..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)

    processed_prompt = user_prompt
    was_swapped = False
    if firewall_active:
        processed_prompt, was_swapped = kavach.intent_swapper(user_prompt)
    
    safe_prompt = kavach.scrub_pii(processed_prompt)

    with st.chat_message("assistant"):
        final_text = ""
        engine_used = ""

        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            if "generate" in user_prompt.lower() or "draw" in user_prompt.lower():
                safe_prompt = f"[0xDETOX_PROVENANCE] {safe_prompt}"
            
            payload = [f"{ZERO_TRAIN_TOKEN}\n\nTask: {safe_prompt}"]
            if up_img:
                payload.append(Image.open(up_img))
            
            response = model.generate_content(payload)
            final_text = response.text
            engine_used = "☁️ Detox Cloud (Gemini)"

        except Exception as e:
            st.warning("Cloud Engine Offline. Activating Local Detox...")
            try:
                res = requests.post("http://localhost:11434/api/generate", 
                                    json={"model": "phi4-mini", "prompt": safe_prompt, "stream": False},
                                    timeout=15)
                final_text = res.json()['response']
                engine_used = "🏠 Local Engine (Ollama)"
            except:
                final_text = "❌ CRITICAL FAILURE: No engines available."
                engine_used = "Offline"

        st.markdown(kavach.restore_pii(final_text))
        st.caption(f"Engine: {engine_used} | Protected by Detox.ai")

    # --- 7. LIVE LOGS FOR JUDGES ---
    with st.expander("🔍 Detox.ai Sovereign Logs (Debug)"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**What you typed:**")
            st.info(user_prompt)
        with col2:
            st.write("**What the AI saw:**")
            st.warning(safe_prompt)
        if was_swapped:
            st.error("⚠️ Intent-Swapper: Malicious Intent neutralized by Detox.ai.")

        st.markdown("### 📋 Document Summary")
        st.write(kavach.restore_pii(final_summary))
        st.caption(f"Engine: {engine} | Protected by Detox.ai")

# --- 6. MAIN LOGIC: CHAT & AUTO-FAILOVER ---
if user_prompt := st.chat_input("Enter directive or ask to generate an image..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)

    processed_prompt = user_prompt
    was_swapped = False
    if firewall_active:
        processed_prompt, was_swapped = kavach.intent_swapper(user_prompt)
    
    safe_prompt = kavach.scrub_pii(processed_prompt)

    with st.chat_message("assistant"):
        final_text = ""
        engine_used = ""

        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            if "generate" in user_prompt.lower() or "draw" in user_prompt.lower():
                safe_prompt = f"[0xDETOX_PROVENANCE] {safe_prompt}"
            
            payload = [f"{ZERO_TRAIN_TOKEN}\n\nTask: {safe_prompt}"]
            if up_img:
                payload.append(Image.open(up_img))
            
            response = model.generate_content(payload)
            final_text = response.text
            engine_used = "☁️ Detox Cloud (Gemini)"

        except Exception as e:
            st.warning("Cloud Engine Offline. Activating Local Detox...")
            try:
                res = requests.post("http://localhost:11434/api/generate", 
                                    json={"model": "phi4-mini", "prompt": safe_prompt, "stream": False},
                                    timeout=15)
                final_text = res.json()['response']
                engine_used = "🏠 Local Engine (Ollama)"
            except:
                final_text = "❌ CRITICAL FAILURE: No engines available."
                engine_used = "Offline"

        st.markdown(kavach.restore_pii(final_text))
        st.caption(f"Engine: {engine_used} | Protected by Detox.ai")

    # --- 7. LIVE LOGS FOR JUDGES ---
    with st.expander("🔍 Detox.ai Sovereign Logs (Debug)"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**What you typed:**")
            st.info(user_prompt)
        with col2:
            st.write("**What the AI saw:**")
            st.warning(safe_prompt)
        if was_swapped:
            st.error("⚠️ Intent-Swapper: Malicious Intent neutralized by Detox.ai.")


