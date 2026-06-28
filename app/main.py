from pathlib import Path
import asyncio
from io import BytesIO
import os
import socket
from xml.sax.saxutils import escape

import qrcode
from qrcode.image.svg import SvgPathImage

from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.config import settings
from app.missions import MISSIONS
from app.state import DemoState, VoteRejected


STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Crowd AI Mission Control")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

demo_state = DemoState()


class VoteRequest(BaseModel):
    vote_type: str
    choice_id: str


class MissionSelectRequest(BaseModel):
    mission_id: str


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[WebSocket, asyncio.Queue[dict[str, object]]] = {}

    async def connect(self, websocket: WebSocket) -> asyncio.Queue[dict[str, object]]:
        await websocket.accept()
        queue: asyncio.Queue[dict[str, object]] = asyncio.Queue()
        self._connections[websocket] = queue
        await queue.put(demo_state.public_state())
        return queue

    def disconnect(self, websocket: WebSocket) -> None:
        self._connections.pop(websocket, None)

    async def broadcast(self, state: dict[str, object]) -> None:
        for queue in self._connections.values():
            await queue.put(state)


manager = ConnectionManager()


def static_file(filename: str) -> FileResponse:
    return FileResponse(STATIC_DIR / filename)


def detect_lan_ip() -> str | None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            ip_address = sock.getsockname()[0]
    except OSError:
        return None
    if ip_address.startswith("127."):
        return None
    return ip_address


def visitor_join_url(request: Request) -> str:
    url = request.url_for("phone")
    hostname = url.hostname or ""
    app_host = os.getenv("APP_HOST", settings.app_host)
    if app_host == "0.0.0.0" and hostname in {"localhost", "127.0.0.1"}:
        lan_ip = detect_lan_ip()
        if lan_ip:
            url = url.replace(netloc=f"{lan_ip}:{url.port}" if url.port else lan_ip)
    return str(url)


@app.get("/")
async def phone() -> FileResponse:
    return static_file("phone.html")


@app.get("/ping")
async def ping() -> PlainTextResponse:
    return PlainTextResponse("pong\n", headers={"Cache-Control": "no-store"})


@app.get("/qr.svg", name="qr_code")
async def qr_code(request: Request) -> Response:
    join_url = visitor_join_url(request)
    image = qrcode.make(
        join_url,
        image_factory=SvgPathImage,
        border=2,
        box_size=12,
    )
    output = BytesIO()
    image.save(output)
    svg = output.getvalue().decode("utf-8")
    title = f"<title>{escape(join_url)}</title><desc>Scan to join the visitor controller.</desc>"
    svg_open = svg.index("<svg")
    svg_open_end = svg.index(">", svg_open)
    svg = f"{svg[:svg_open_end + 1]}{title}{svg[svg_open_end + 1:]}"
    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={"Cache-Control": "no-store"},
    )


@app.get("/screen")
async def screen() -> FileResponse:
    return static_file("screen.html")


@app.get("/staff")
async def staff() -> FileResponse:
    return static_file("staff.html")


@app.get("/replay")
async def replay() -> FileResponse:
    return static_file("replay.html")


@app.get("/health")
async def health() -> dict[str, object]:
    return {
        "status": "healthy",
        "mode": demo_state.public_state()["mode"],
        "app_port": settings.app_port,
        "missions_loaded": len(MISSIONS),
        "model_enabled": settings.model_enabled,
    }


@app.get("/api/state")
async def api_state() -> dict[str, object]:
    return demo_state.public_state()


@app.get("/api/join-url")
async def api_join_url(request: Request) -> dict[str, str]:
    return {"url": visitor_join_url(request)}


@app.post("/api/vote")
async def vote(request: VoteRequest) -> dict[str, object]:
    try:
        state = demo_state.submit_vote(request.vote_type, request.choice_id)
    except VoteRejected as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    await manager.broadcast(state)
    return state


@app.post("/api/staff/select-mission")
async def select_mission(request: MissionSelectRequest) -> dict[str, object]:
    try:
        state = demo_state.select_mission(request.mission_id)
    except VoteRejected as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    await manager.broadcast(state)
    return state


@app.post("/api/staff/advance")
async def advance() -> dict[str, object]:
    state = demo_state.advance()
    await manager.broadcast(state)
    return state


@app.post("/api/staff/reset")
async def reset() -> dict[str, object]:
    state = demo_state.reset()
    await manager.broadcast(state)
    return state


@app.post("/api/staff/fallback")
async def fallback() -> dict[str, object]:
    state = demo_state.fallback()
    await manager.broadcast(state)
    return state


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    queue = await manager.connect(websocket)
    try:
        while True:
            await websocket.send_json(await queue.get())
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except RuntimeError:
        manager.disconnect(websocket)
