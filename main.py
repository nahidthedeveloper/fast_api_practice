from fastapi import FastAPI, Request, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket
import datetime
import uvicorn
import os

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


@app.on_event("startup")
async def startup_event():
    print('Server started :', datetime.datetime.now())


@app.on_event("shutdown")
async def shutdown_event():
    print('server Shutdown :', datetime.datetime.now())


@app.get("/media")
async def list_media_files():
    media_dir = "media"
    if not os.path.exists(media_dir):
        return JSONResponse(content={"error": "Media directory not found"}, status_code=404)

    # Get a list of all files in the media directory
    files = [f for f in os.listdir(media_dir) if os.path.isfile(os.path.join(media_dir, f))]
    return {"files": files}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("WebSocket disconnected")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("socket.html", {"request": request})


@app.get('/hello')  # Example: http://127.0.0.1:8000/hello?name=nahid&age=25
async def hello(name: str, age: int):
    return {"message": f"Hello {name}, Your age {age}"}


@app.get('/hello/{name}')
async def hello_path(name: str):
    return {"message": f"Hello {name}"}
