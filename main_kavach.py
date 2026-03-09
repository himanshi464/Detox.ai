import ollama
from kavach_scrubber import scrub_text  # Importing your filter logic

def start_kavach():
    print("================================================")
    print("🛡️  KAVACH-AI: ATMANIRBHAR SECURITY MIDDLEWARE  🛡️")
    print("        (Sovereign Inference Mode Active)       ")
    print("================================================\n")
    
    while True:
        user_prompt = input("👤 Enter your query (or 'exit'): ")
        
        if user_prompt.lower() == 'exit':
            break

        # STAGE 1: SCRUBBING (Data Minimization)
        # This prevents PII from reaching the AI model context
        secure_prompt = scrub_text(user_prompt)
        
        print(f"\n🔒 [KAVACH-SHIELD]: Redacting PII...")
        print(f"📡 [DATA SENT TO AI]: {secure_prompt}\n")

        # STAGE 2: LOCAL INFERENCE
        try:
            response = ollama.chat(model='phi4-mini', messages=[
                {'role': 'system', 'content': 'You are KAVACH-AI. Provide security-focused guidance using the provided redacted context.'},
                {'role': 'user', 'content': secure_prompt},
            ])
            
            print(f"🤖 KAVACH-AI RESPONSE:\n{response['message']['content']}\n")
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ Connection Error: Ensure Ollama is running. ({e})")

if __name__ == "__main__":
    start_kavach()
    