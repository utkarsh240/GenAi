# main.py
from .server import app
import uvicorn

def main():
    uvicorn.run(app, port=8000, host="0.0.0.0")

main()
