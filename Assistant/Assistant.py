#import modules
import os
import re
import time
import logging
from typing import Optional
from fastapi import FastAPI, Request, HTTPException, Depends, Header
from pydantic import BaseModel
import requests
import jwt

# Configuration
OPENAI_AI_KEY = os.environ.get("OPEN_API_KEY")
JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret")
AUDIT_LOG = os.environ.get("AUDIT_LOG", "audit.log")

# Logging Configuration
logger = logging.getLogger("assistant")
logger.setLevel(logging.INFO)
fh = logging.FileHandler(AUDIT_LOG)
fh.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
logger.addHandler(fh)

# FastAPI
app = FastAPI(title="Personal Intelligence Assistant")

# Model
class ChatRequest(BaseModel):
    query: str
    user_id: str
    context_id: Optional[str] = None  # optional retrieval context

class ChatResponse(BaseModel):
    reply: str
    model: str = "gpt-4o"  # example; choose appropriate model in prod

# --- Simple RBAC / JWT verification ---
def verify_jwt(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(401, "Missing Authorization header")
    token = authorization.removeprefix("Bearer ").strip()
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except Exception as e:
        raise HTTPException(401, "Invalid token")
    # minimal payload check
    if payload.get("role") not in ("agent", "officer", "admin"):
        raise HTTPException(403, "Insufficient role")
    return payload

# --- Basic PII redaction (customize!) ---
PII_PATTERNS = [
    (re.compile(r"\b\d{9,16}\b"), "<REDACTED_NUMBER>"),  # long numeric sequences
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "<REDACTED_EMAIL>"),
    # Add phone, SSN, names patterns as required (careful with false positives)
]

def redact_pii(text: str) -> str:
    for pat, repl in PII_PATTERNS:
        text = pat.sub(repl, text)
    return text

# --- Audit logging helper ---
def audit_event(user_id: str, action: str, metadata: dict):
    logger.info({"user_id": user_id, "action": action, "meta": metadata})

# --- OpenAI call (simple) ---
OPENAI_CHAT_ENDPOINT = "https://api.openai.com/v1/chat/completions"

def call_openai_chat_system(prompt: str, system_instructions: str = "You are a helpful, concise assistant.") -> str:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    # messages format (Chat Completions)
    body = {
      "model": "gpt-4o-mini",   # pick model per policy and cost; change as needed
      "messages": [
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": prompt}
      ],
      "max_tokens": 800,
      "temperature": 0.2
    }
    r = requests.post(OPENAI_CHAT_ENDPOINT, json=body, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    # navigate response safely
    return data["choices"][0]["message"]["content"]

# --- Endpoint: chat ---
@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest, token_payload = Depends(verify_jwt)):
    user_id = req.user_id
    # 1) redact incoming PII before sending to logs or LLM (policy dependent)
    redacted_query = redact_pii(req.query)
    audit_event(user_id, "query_received", {"original_len": len(req.query), "redacted": redacted_query[:200]})

    # 2) optional: retrieve documents for context (RAG hook)
    # For now we simply append a short context hint. Replace with vector DB lookups.
    context_text = ""
    if req.context_id:
        # placeholder — integrate FAISS/Chroma retrieval here
        context_text = f"\n[Context {req.context_id}: classified doc summary goes here]\n"

    prompt = f"{context_text}\nUser query: {redacted_query}\nProvide a clear, factual response. If the query requests disallowed info, refuse and escalate."

    # 3) make the call (backend-only)
    try:
        reply = call_openai_chat_system(prompt)
    except requests.HTTPError as e:
        audit_event(user_id, "openai_error", {"error": str(e)})
        raise HTTPException(502, "AI backend error")
    # 4) redact any PII from model output before returning or logging
    redacted_reply = redact_pii(reply)
    audit_event(user_id, "reply_sent", {"reply_preview": redacted_reply[:200]})
    return ChatResponse(reply=redacted_reply, model="gpt-4o-mini")




