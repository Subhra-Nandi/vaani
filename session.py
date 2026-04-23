import redis
import json
import uuid

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def create_session(student_id: str) -> str:
    session_id = str(uuid.uuid4())
    state = {
        "student_id": student_id,
        "turn": 0,
        "current_state": "GREETING",
        "objections": [],
        "commitment_made": False,
        "lms_context": {
            "student_name": "Rohan",
            "last_module": "Fractions",
            "score": "40%",
            "days_since_login": 5
        }
    }
    r.setex(f"session:{session_id}", 3600, json.dumps(state))
    return session_id

def get_session(session_id: str) -> dict:
    data = r.get(f"session:{session_id}")
    return json.loads(data) if data else None

def update_session(session_id: str, updates: dict):
    session = get_session(session_id)
    session.update(updates)
    session["turn"] += 1
    r.setex(f"session:{session_id}", 3600, json.dumps(session))