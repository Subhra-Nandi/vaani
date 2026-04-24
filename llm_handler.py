import ollama

SYSTEM_PROMPT = """You are a warm Hindi educational assistant. Reply ONLY in simple Hinglish (mix of Hindi and English).
Keep it to exactly 2 sentences.
Sentence 1: Show empathy about their problem.
Sentence 2: Gently ask if they can study a little bit today.
Never ask unrelated questions. Always end with a study-related question.

Example input: "meri tabiyat theek nahi"
Example output: "Arre, tabiyat kharab hai to aaram karo. Jab thoda better feel karo, kya 10 minute Fractions dekh sakte hain?"
"""

def handle_objection(user_text: str, session_context: dict) -> str:
    context_str = f"Student last studied: {session_context['lms_context']['last_module']}, score: {session_context['lms_context']['score']}"
    
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context: {context_str}\nStudent said: {user_text}"}
        ]
    )
    return response['message']['content']

if __name__ == "__main__":
    test_session = {
        "lms_context": {"last_module": "Fractions", "score": "40%"}
    }
    print(handle_objection("meri dadi beemar hain", test_session))