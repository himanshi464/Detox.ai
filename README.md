🛡️ Detox.ai: Sovereign Data Shield
India Innovates 2026 | Track: Cybersecurity

Detox.ai is a privacy-first middleware designed to "detoxify" user prompts by stripping out sensitive PII (Personally Identifiable Information) before they reach the cloud. It ensures that constitutional and ministerial data remains sovereign while still leveraging the power of Large Language Models.

🚀 Key Features
1. 🛡️ Sovereign Privacy Engine (Local-First)
PII Scrubbing: Automatically detects and masks Indian identity markers (Aadhaar, PAN, Mobile) using local regex-based interception.

Consistent Dummy Mapping: Replaces real data with tags like <AADHAAR_ID_1>. The AI maintains logical consistency, but never sees the actual values.

Round-Trip Restoration: Real data is "unmasked" only on the local UI after the AI responds, keeping the cloud in the dark.

2. 🤖 Intelligent Failover & Multimodal
Auto-Switching Engine: If the Cloud API (Gemini) fails due to 404/400 errors or connectivity issues, Detox.ai automatically triggers a local failover to Ollama (Phi-4).

Vision AI Extraction: Securely "reads" and sanitizes data from images of ID cards locally before sending sanitized text for processing.

3. 🌐 Advanced Guardrails
Zero-Training Policy: Injects a policy-enforcement token into every prompt to disable provider-side data logging and training.

Memetic Firewall: A simulated Chrome Extension that neutralizes risky queries (e.g., tax evasion) into safe, legal alternatives locally.

Stochastic Noise Injection: Adds "Differential Privacy" by inserting random words into prompts to prevent LLM token memorization.

🛠️ Tech Stack
Frontend: Streamlit (Sovereign OS Interface)

Cloud AI: Google Gemini 1.5 Flash (Sovereign Cloud)

Local AI: Ollama (Running Phi-4-mini)

Security: Python-based Regex & Stochastic Noise Injection
