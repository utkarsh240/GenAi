from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def chat():
    return {"status: Server is up and running"}

@app.post('/chat')
def chat():
    pass