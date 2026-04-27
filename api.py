from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json
from session import create_session, get_session, update_session
from dialogue import get_next_response

app = FastAPI(title="Vaani — Hindi Voice Agent API")
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

class StartSessionRequest(BaseModel):
    student_id: str
    student_name: str
    last_module: str
    score: str

class TurnRequest(BaseModel):
    session_id: str
    user_text: str

@app.post("/session/start")
def start_session(req: StartSessionRequest):
    session_id = create_session(req.student_id)
    session = get_session(session_id)
    session["lms_context"]["student_name"] = req.student_name
    session["lms_context"]["last_module"] = req.last_module
    session["lms_context"]["score"] = req.score
    r.setex(f"session:{session_id}", 3600, json.dumps(session))
    return {
        "session_id": session_id,
        "opening_message": f"Namaste {req.student_name}! Main TAP ki taraf se bol raha hoon.",
        "current_state": "GREETING"
    }

@app.post("/session/turn")
def process_turn(req: TurnRequest):
    result = get_next_response(req.session_id, req.user_text)
    session = get_session(req.session_id)
    return {
        "reply": result["reply"],
        "next_state": result["next_state"],
        "intent": result["intent"],
        "is_terminal": result["is_terminal"],
        "turn_number": session["turn"]
    }

@app.get("/session/{session_id}")
def get_session_state(session_id: str):
    return get_session(session_id)

@app.post("/queue/push")
def push_to_queue(student_id: str):
    r.lpush("call_queue", student_id)
    return {"queued": student_id, "queue_length": r.llen("call_queue")}

@app.get("/queue/next")
def pop_from_queue():
    student_id = r.rpop("call_queue")
    return {"next_student": student_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)