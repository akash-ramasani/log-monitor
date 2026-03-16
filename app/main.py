from fastapi import FastAPI, HTTPException, Query

from app.log_reader import resolve_log_path, tail_lines

app = FastAPI(title="Log Monitor API")


@app.get("/")
def root():
    return {
        "message": "Log Monitor API is running"
    }


@app.get("/logs")
def get_logs(
    filename: str = Query(..., description="Path under var/log, e.g. apache/log3.txt"),
    limit: int = Query(100, ge=1, le=10000, description="Number of newest entries to return"),
    keyword: str | None = Query(None, description="Optional substring filter"),
):
    try:
        file_path = resolve_log_path(filename)
        lines = tail_lines(file_path=file_path, limit=limit, keyword=keyword)

        return {
            "filename": filename,
            "limit": limit,
            "keyword": keyword,
            "count": len(lines),
            "entries": lines,
        }

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="log file not found")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=500, detail="internal server error")
