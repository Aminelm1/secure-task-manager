from fastapi import FastAPI

app = FastAPI(
    title="Secure Task Manager API",
    description="SaaS Task Manager secured with IAM and deployed with DevOps tools.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Secure Task Manager API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }