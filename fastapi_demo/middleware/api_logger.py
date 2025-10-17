import json
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi_demo.mongodb import api_call_log
# Reuse the connection (avoid creating per request)

class APILoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # --- 1. Capture request ---
        request_body = await request.body()
        # clone the request stream to avoid consuming it.
        request = Request(request.scope, receive=lambda: {"type": "http.request", "body": request_body})
        user_id = request.headers.get("X-User-Id")  # or extract from JWT

        log_entry = {
            "user_id": user_id,
            "method": request.method,
            "url": str(request.url),
            "request_data": {},
            "response_data": {},
            "date_created": datetime.utcnow(),
        }

        try:
            # Parse query and body safely
            log_entry["request_data"] = {
                "query": dict(request.query_params),
                "body": json.loads(request_body.decode()) if request_body else None,
                "headers": dict(request.headers),
            }
        except Exception:
            log_entry["request_data"] = {"raw_body": str(request_body)}

        # --- 2. Execute the endpoint ---
        response = await call_next(request)

        # --- 3. Capture response ---
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        response.body_iterator = iter([response_body])  # reassign for downstream use

        try:
            response_json = json.loads(response_body.decode())
        except Exception:
            response_json = response_body.decode(errors="ignore")

        log_entry["response_data"] = {
            "status_code": response.status_code,
            "body": response_json if isinstance(response_json, dict) else str(response_json)[:500],
            # truncate long bodies
        }

        # --- 4. Insert into MongoDB ---
        api_call_log.insert_one(log_entry)

        # --- 5. Return response ---
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
