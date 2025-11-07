# make_token.py (dev only)
import jwt, os, time
JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret")
payload = {"sub": "agent_001", "role": "agent", "iat": int(time.time()), "exp": int(time.time()) + 3600}
print("Bearer " + jwt.encode(payload, JWT_SECRET, algorithm="HS256"))
