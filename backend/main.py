from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.agent import run_agent
from utils.context import session_id_context
import io
import pandas as pd
from memory.session_store import save_dataframe

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.get("/health")
def health_check():
    return {"Status" : "ok"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        session_id_context.set(request.session_id)
        res = run_agent(request.message)
        return {"response" : res}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"response": f"An error occurred: {str(e)}"}
        )
    
@app.post("/upload")
async def upload(file: UploadFile = File(...), session_id: str = Form(...)):
    """
    Accepts a CSV file upload, processes it into a pandas DataFrame in memory,
    and links it to the provided session_id.
    """
    if not file.filename.endswith('.csv'):
        return JSONResponse(status_code=400, content={"response": "Only CSV files are supported."})
    
    try:
        # 2. Read the raw bytes from the uploaded file
        contents = await file.read()
        
        # 3. Decode bytes to string -> wrap in StringIO -> load into pandas
        csv_data = contents.decode("utf-8")
        df = pd.read_csv(io.StringIO(csv_data))
        
        # Clean up entirely empty rows/columns if necessary
        df = df.dropna(how="all")

        # 4. Persist the DataFrame to the shared session store
        save_dataframe(session_id, df)

        return {
            "response": f"Successfully uploaded and processed '{file.filename}'."
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"response": f"An error occurred: {str(e)}"})
    finally:
        await file.close()