import asyncio
import io
import logging
from typing import Optional
from fastapi import FastAPI, File, Form, UploadFile, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

from agent.agent import run_agent
from utils.context import session_id_context
from memory.session_store import save_dataframe
from memory.session_auth import auth_manager

logger = logging.getLogger("quantly.api")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Quantly API")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    session_id: str
    session_token: Optional[str] = None


def verify_request_session(
    session_id: str,
    session_token: Optional[str] = None,
    x_session_token: Optional[str] = None,
    authorization: Optional[str] = None,
) -> bool:
    """Verifies that the caller possesses a valid bearer token for the specified session_id."""
    token = session_token or x_session_token
    if not token and authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1]
    return auth_manager.validate_session(session_id, token)


@app.get("/health")
def health_check():
    return {"Status": "ok"}


@app.post("/session")
def create_session():
    """Issues a server-authorized anonymous session ID and a high-entropy bearer token."""
    session_id, session_token = auth_manager.create_session()
    return {"session_id": session_id, "session_token": session_token}


@app.post("/chat")
async def chat(
    request: ChatRequest,
    x_session_token: Optional[str] = Header(None, alias="X-Session-Token"),
    authorization: Optional[str] = Header(None),
):
    if not verify_request_session(
        request.session_id,
        request.session_token,
        x_session_token,
        authorization,
    ):
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized: Invalid or missing session credentials."},
        )

    try:
        def _invoke_agent():
            session_id_context.set(request.session_id)
            return run_agent(request.message, session_id=request.session_id)

        # Offload synchronous LLM/tools call to a worker thread so the async event loop is never blocked
        res = await asyncio.wait_for(asyncio.to_thread(_invoke_agent), timeout=60.0)
        return {"response": res}
    except asyncio.TimeoutError:
        logger.error("Chat request timed out for session: %s", request.session_id)
        return JSONResponse(
            status_code=504,
            content={"response": "The request timed out while generating a response. Please try again."},
        )
    except Exception as e:
        logger.exception("Error during chat request: %s", str(e))
        return JSONResponse(
            status_code=500,
            content={"response": "An unexpected error occurred while processing your request. Please try again later."},
        )


@app.post("/upload")
async def upload(
    file: UploadFile = File(...),
    session_id: str = Form(...),
    session_token: Optional[str] = Form(None),
    x_session_token: Optional[str] = Header(None, alias="X-Session-Token"),
    authorization: Optional[str] = Header(None),
):
    """
    Accepts a CSV file upload, processes it into a pandas DataFrame in memory,
    and links it to the authorized session_id.
    """
    if not verify_request_session(
        session_id,
        session_token,
        x_session_token,
        authorization,
    ):
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized: Invalid or missing session credentials."},
        )

    if not file.filename.endswith(".csv"):
        return JSONResponse(
            status_code=400,
            content={"response": "Only CSV files are supported."},
        )

    try:
        contents = await file.read()
        csv_data = contents.decode("utf-8", errors="replace")
        df = pd.read_csv(io.StringIO(csv_data))
        df = df.dropna(how="all")

        save_dataframe(session_id, df)

        return {
            "response": f"Successfully uploaded and processed '{file.filename}'."
        }
    except Exception as e:
        logger.exception("Error processing uploaded file: %s", str(e))
        return JSONResponse(
            status_code=500,
            content={"response": "Failed to process the uploaded CSV file."},
        )
    finally:
        await file.close()