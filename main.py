import time
from session import create_session, get_session
from stt import record_audio, transcribe
from tts import speak
from lang_detect import detect_language
from dialogue import get_next_response, STATES


def play_greeting(session_id: str):
    session = get_session(session_id)
    greeting = STATES["GREETING"]["entry_message"].format(
        name=session["lms_context"]["student_name"],
        module=session["lms_context"]["last_module"],
        score=session["lms_context"]["score"]
    )
    print(f"\nBot: {greeting}")
    speak(greeting)


def run_conversation(student_id: str = "TAP-9821"):
    print(f"\n=== Starting Vaani session for {student_id} ===\n")
    session_id = create_session(student_id)

    play_greeting(session_id)

    max_turns = 8

    for turn in range(max_turns):
        print(f"\n[Turn {turn + 1}] Listening...")

        audio, sr = record_audio(seconds=6)
        user_text = transcribe(audio, sr)

        if not user_text.strip() or len(user_text.strip()) < 2:
            print("(no speech detected, listening again...)")
            continue

        lang = detect_language(user_text)
        print(f"User ({lang}): {user_text}")

        result = get_next_response(session_id, user_text)

        print(f"Bot [{result['next_state']}]: {result['reply']}")

        if result['reply']:
            speak(result['reply'])
            time.sleep(1.5)

        if result['is_terminal']:
            print("\n=== Conversation complete ===")
            break

        time.sleep(0.5)


if __name__ == "__main__":
    run_conversation()