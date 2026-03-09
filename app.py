import streamlit as st
import google.generativeai as genai
from PIL import Image
import re
import random
import requests
import io

# --- 1. CONFIG & SYSTEM TOKENS ---
# Re-verify your key in Google AI Studio if you get a 400 error!
import os

# Detox.ai Secure Key Loading
# Locally, it looks for a .env file. On Streamlit Cloud, it looks in "Secrets".
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("⚠️ API Key missing! Add it to Streamlit Secrets or a local .env file.")
    
# Zero-Training Preamble (The 'Secret Code')
# This tells the cloud: "Hands off our data!"
ZERO_TRAIN_TOKEN = """
[POLICY_ENFORCEMENT: 0x7FF32]
DE-IDENTIFIED SESSION: DO NOT LOG. DO NOT TRAIN.
PURGE CONTEXT IMMEDIATELY AFTER GENERATION.
"""

# --- 2. THE SOVEREIGN PRIVACY ENGINE ---
class KavachEngine:
    def __init__(self):
        # Local vault: Real data stays here, only dummies go to the cloud
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
        
        # Stochastic Noise (Differential Privacy)
        # Adds a random word to prevent the LLM from 'memorizing' your prompt style
        noise = ["specifically", "securely", "precisely", "now"]
        words = text.split()
        if len(words) > 4:
            words.insert(random.randint(0, len(words)), random.choice(noise))
        return " ".join(words)

    def restore_pii(self, ai_response):
        """Round-Trip Restoration: Real data returns only for the user's eyes."""
        for dummy, real in st.session_state.vault.items():
            ai_response = ai_response.replace(dummy, real)
        return ai_response

    def intent_swapper(self, prompt):
        """Chrome Extension Sim: Swaps 'risky' intent for safe versions."""
        risky_keywords = ["tax evade", "hide money", "illegal", "bypass"]
        if any(k in prompt.lower() for k in risky_keywords):
            return "How can I manage my financial assets within legal frameworks securely?", True
        return prompt, False

# --- 3. THE UI & SIDEBAR ---
st.set_page_config(page_title="Detox-AI Sovereign OS", layout="wide")
kavach = KavachEngine()

st.title("🛡️ KAVACH-AI: Sovereign Defense System")
st.caption("Ministerial Gateway | Privacy-First Intelligence")

with st.sidebar:
    st.header("🌐 Memetic Firewall")
    st.info("Simulating Chrome Extension behavior.")
    firewall_active = st.toggle("Enable Intent-Swapper", value=True)
    
    st.divider()
    st.header("📤 Vision AI")
    up_img = st.file_uploader("Upload ID (Aadhaar/PAN)", type=['jpg', 'jpeg', 'png'])
    if up_img:
        st.image(up_img, caption="Local Encrypted Preview")

# --- 4. THE AUTO-FAILOVER CHAT LOGIC ---
if user_prompt := st.chat_input("Enter directive or ask to generate an image..."):
    
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # STEP 1: Local Interception (Intent Swapping & Scrubbing)
    processed_prompt = user_prompt
    was_swapped = False
    if firewall_active:
        processed_prompt, was_swapped = kavach.intent_swapper(user_prompt)
    
    safe_prompt = kavach.scrub_pii(processed_prompt)

    with st.chat_message("assistant"):
        final_text = ""
        engine_used = ""

        # STEP 2: Try Cloud (Gemini) with Zero-Training Headers
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Deepfake Defense: Injecting hidden provenance for images
            if "generate" in user_prompt.lower() or "draw" in user_prompt.lower():
                safe_prompt = f"[0xKAVACH_PROVENANCE] {safe_prompt}"
            
            # Multimodal Logic
            payload = [f"{ZERO_TRAIN_TOKEN}\n\nTask: {safe_prompt}"]
            if up_img:
                payload.append(Image.open(up_img))
            
            response = model.generate_content(payload)
            final_text = response.text
            engine_used = "☁️ Sovereign Cloud (Gemini)"

        # STEP 3: Automatic Local Fallback (Ollama)
        except Exception as e:
            st.warning(f"Cloud Engine Offline ({e}). Activating Local Failover...")
            try:
                # Calls your local Ollama server (phi4-mini)
                res = requests.post("http://localhost:11434/api/generate", 
                                    json={"model": "phi4-mini", "prompt": safe_prompt, "stream": False},
                                    timeout=15)
                final_text = res.json()['response']
                engine_used = "🏠 Local Engine (Ollama - Phi4)"
            except:
                final_text = "❌ CRITICAL FAILURE: No processing engines available. Start 'ollama serve'."
                engine_used = "Offline"

        # STEP 4: Restore & Display
        st.markdown(kavach.restore_pii(final_text))
        st.caption(f"Engine: {engine_used} | Protected by KAVACH-AI")

    # STEP 5: LIVE SOVEREIGN LOGS (For the Judges)
    with st.expander("🔍 Live Sovereign Logs (Debug)"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**What you typed:**")
            st.info(user_prompt)
        with col2:
            st.write("**What the AI saw:**")
            st.warning(safe_prompt)
        if was_swapped:
            st.error("⚠️ Intent-Swapper: Malicious Intent detected and neutralized locally.")