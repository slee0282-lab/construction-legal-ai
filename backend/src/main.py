from fastapi import FastAPI
import redis
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Construction Legal AI Backend"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/redis-test")
def redis_test():
    try:
        redis_host = os.getenv("REDIS_HOST", "localhost")
        r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        r.ping()
        return {"status": "connected", "host": redis_host}
    except Exception as e:
        return {"status": "error", "message": str(e)}
