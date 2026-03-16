from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

from app.log_reader import resolve_log_path, tail_lines

app = FastAPI(title="Log Monitor API")

UI_FILE = Path(__file__).resolve().parent / "ui" / "index.html"


@app.get("/")
def root():
    return {"message": "Log Monitor API is running"}


@app.get("/ui")
def ui():
    return FileResponse(UI_FILE)


@app.get("/logs")
def get_logs(
    filename: str = Query(..., description="Path under var/log, e.g. apache/log3.txt"),
    limit: int = Query(100, ge=1, le=10000, description="Number of newest entries to return"),
    keyword: str | None = Query(None, description="Optional substring filter"),
):
    try:
        file_path = resolve_log_path(filename)
        lines = tail_lines(file_path=file_path, limit=limit, keyword=keyword)

        cleaned_lines = [line for line in lines if line.strip() != ""]

        return {
            "filename": filename,
            "limit": limit,
            "keyword": keyword,
            "count": len(cleaned_lines),
            "entries": cleaned_lines,
        }

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="log file not found")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=500, detail="internal server error")
