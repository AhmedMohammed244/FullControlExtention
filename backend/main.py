from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from pipeline import Pipeline

app = FastAPI()

pipe = Pipeline()


class AnalyzeRequest(BaseModel):

    source: str


@app.post("/analyze")
def analyze(req: AnalyzeRequest):

    try:

        task = pipe.run(req.source)

        return {
            "task_id": task.id,
            "workspace": str(task.workspace),
            "audio": str(task.audio),
            "cached": task.cached,
            "status": task.status
        }

    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))