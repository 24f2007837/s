import time
import uuid
from typing import List
from fastapi import FastAPI, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- Strict CORS Configuration ---
# Only allow your explicitly assigned origin
ALLOWED_ORIGIN = "https://dash-eq14wx.example.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# --- Required Middleware for Custom Headers ---
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.perf_counter()
    
    # Generate unique Request ID
    request_id = str(uuid.uuid4())
    
    # Process the request
    response: Response = await call_next(request)
    
    # Calculate duration
    process_time = time.perf_counter() - start_time
    
    # Inject required headers into every response
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    
    return response

# --- Stats Endpoint ---
@app.get("/stats")
def get_stats(values: str = Query(..., description="Comma-separated integers")):
    # Parse the comma-separated integers dynamically
    try:
        int_values: List[int] = [int(v.strip()) for v in values.split(",") if v.strip()]
    except ValueError:
        return Response(content='{"error": "Invalid integers provided"}', status_code=400, media_type="application/json")

    if not int_values:
        return Response(content='{"error": "Empty values list"}', status_code=400, media_type="application/json")

    # Compute descriptive statistics
    count_n = len(int_values)
    sum_s = sum(int_values)
    min_m = min(int_values)
    max_x = max(int_values)
    mean_f = sum_s / count_n

    # Formulate payload response (Replace with your actual logged-in email address)
    payload = {
        "email": "your-email@example.com", 
        "count": count_n,
        "sum": sum_s,
        "min": min_m,
        "max": max_x,
        "mean": round(mean_f, 4)  # Comfortably within the ±0.01 threshold
    }
    
    return payload