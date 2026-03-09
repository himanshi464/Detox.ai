import ollama

def sovereign_check():
    print("🛡️ --- KAVACH-AI: PHASE 1 SOVEREIGN NODE ---")
    
    # This proves the local model (Phi-4-mini) is reachable
    prompt = "chocolate"
    
    print(f"\nSending Local Query: {prompt}")
    
    try:
        response = ollama.chat(model='phi4-mini', messages=[
            {'role': 'user', 'content': prompt},
        ])
        print("\n🤖 LOCAL AI RESPONSE:")
        print(response['message']['content'])
        print("\n✅ PHASE 1 VERIFIED: System is Atmanirbhar.")
    except Exception as e:
        print(f"\n❌ ERROR: Ensure Ollama is running and Phi-4-mini is pulled. Details: {e}")

if __name__ == "__main__":
    sovereign_check()