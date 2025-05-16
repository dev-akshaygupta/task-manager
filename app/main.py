from fastapi import FastAPI

app = FastAPI()

@app.get("/home")
def home():
    return {"message": "This is home page for personal task manager application."}