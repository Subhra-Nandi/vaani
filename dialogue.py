from session import get_session, update_session

STATES = {
    "GREETING": {
        "entry_message": "Namaste {name}! Main TAP ki taraf se bol raha hoon. Kya aap abhi baat kar sakte hain?",
        "transitions": {
            "yes_keywords": ["haan", "ha", "theek", "okay", "boliye", "bolo", "हाँ", "हां", "ठीक", "ओके"],
            "no_keywords": ["nahi", "baad", "busy", "time nahi","नहीं", "बाद", "बिज़ी"],
            "on_yes": "LMS_CONTEXT",
            "on_no": "RESCHEDULE",
            "default": "GREETING_RETRY"
        }
    },
    "LMS_CONTEXT": {
        "entry_message": "Aapne {module} abhi tak complete nahi kiya. Aapka score {score} hai. Kya aaj thoda time nikal sakte hain?",
        "transitions": {
            "yes_keywords": ["haan", "karunga", "karungi", "theek hai", "try", "हाँ", "हां", "ठीक", "ओके"],
            "no_keywords": ["nahi", "kal", "time nahi", "baad mein", "नहीं", "कल", "समय नहीं", "बाद में"],
            "on_yes": "COMMITMENT",
            "on_no": "OBJECTION_HANDLER",
            "default": "OBJECTION_HANDLER"
        }
    },
    "COMMITMENT": {
        "entry_message": "Bahut accha! Kya aap aaj shaam 7 baje module kholenge?",
        "transitions": {
            "yes_keywords": ["haan", "zaroor", "bilkul", "pakka", "हाँ", "ज़रूर", "बिल्कुल", "पक्का"],
            "no_keywords": ["nahi", "pata nahi", "shayad", "नहीं", "पता नहीं", "शायद"],
            "on_yes": "CLOSING_POSITIVE",
            "on_no": "CLOSING_SOFT",
            "default": "CLOSING_SOFT"
        }
    },
    "RESCHEDULE": {
        "entry_message": "Koi baat nahi. Kya main kal shaam call karun?",
        "transitions": {
            "yes_keywords": ["haan", "theek", "okay"],
            "no_keywords": ["nahi"],
            "on_yes": "CLOSING_POSITIVE",
            "on_no": "CLOSING_SOFT",
            "default": "CLOSING_POSITIVE"
        }
    },
    "OBJECTION_HANDLER": {
        "entry_message": None,
        "transitions": {
            "on_complete": "COMMITMENT"
        }
    },
    "CLOSING_POSITIVE": {
        "entry_message": "Shukriya! Aap bahut accha kar rahe hain. All the best!",
        "transitions": {}
    },
    "CLOSING_SOFT": {
        "entry_message": "Theek hai. Yaad rakhein, TAP hamesha aapke saath hai.",
        "transitions": {}
    },
    "GREETING_RETRY": {
    "entry_message": "Kya aap mujhe sun pa rahe hain? Kripya 'haan' ya 'nahi' mein jawab dein.",
    "transitions": {
        "yes_keywords": ["haan", "ha", "sun", "हाँ", "हां", "हा"],
        "no_keywords": ["nahi", "नहीं"],
        "on_yes": "LMS_CONTEXT",
        "on_no": "CLOSING_SOFT",
        "default": "CLOSING_SOFT"
    }
},
}

def classify_input(text: str, transitions: dict) -> str:
    text_lower = text.lower()
    for kw in transitions.get("yes_keywords", []):
        if kw in text_lower:
            return "yes"
    for kw in transitions.get("no_keywords", []):
        if kw in text_lower:
            return "no"
    return "default"

def get_next_response(session_id: str, user_text: str) -> dict:
    session = get_session(session_id)
    current_state = session["current_state"]
    state_config = STATES[current_state]
    transitions = state_config.get("transitions", {})

    intent = classify_input(user_text, transitions)

    if intent == "yes" and "on_yes" in transitions:
        next_state = transitions["on_yes"]
    elif intent == "no" and "on_no" in transitions:
        next_state = transitions["on_no"]
    elif "default" in transitions:
        next_state = transitions["default"]
    else:
        next_state = "CLOSING_SOFT"

    next_state_config = STATES[next_state]
    reply_template = next_state_config.get("entry_message", "")

    reply = reply_template.format(
        name=session["lms_context"].get("student_name", ""),
        module=session["lms_context"]["last_module"],
        score=session["lms_context"]["score"]
    ) if reply_template else ""

    update_session(session_id, {
        "current_state": next_state,
        "objections": session["objections"] + ([user_text] if intent == "no" else [])
    })

    return {
        "reply": reply,
        "next_state": next_state,
        "intent": intent,
        "is_terminal": not bool(next_state_config.get("transitions"))
    }