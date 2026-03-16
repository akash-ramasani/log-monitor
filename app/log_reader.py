from pathlib import Path
from typing import List, Optional


BASE_LOG_DIR = (Path(__file__).resolve().parent.parent / "var" / "log").resolve()


def resolve_log_path(filename: str) -> Path:
    if not filename:
        raise ValueError("filename is required")

    candidate = (BASE_LOG_DIR / filename).resolve()

    if not str(candidate).startswith(str(BASE_LOG_DIR)):
        raise ValueError("invalid filename path")

    if not candidate.exists():
        raise FileNotFoundError(f"file not found: {filename}")

    if not candidate.is_file():
        raise ValueError("path is not a file")

    return candidate


def tail_lines(
    file_path: Path,
    limit: int = 100,
    keyword: Optional[str] = None,
    chunk_size: int = 8192,
    encoding: str = "utf-8",
) -> List[str]:
    if limit <= 0:
        return []

    keyword_bytes = keyword.encode(encoding) if keyword else None
    results: List[str] = []

    with file_path.open("rb") as f:
        f.seek(0, 2)
        file_size = f.tell()

        buffer = b""
        position = file_size

        while position > 0 and len(results) < limit:
            read_size = min(chunk_size, position)
            position -= read_size
            f.seek(position)

            chunk = f.read(read_size)
            buffer = chunk + buffer

            lines = buffer.split(b"\n")

            buffer = lines[0]

            for raw_line in reversed(lines[1:]):
                if keyword_bytes and keyword_bytes not in raw_line:
                    continue

                line = raw_line.decode(encoding, errors="replace")
                results.append(line)

                if len(results) >= limit:
                    break

        if len(results) < limit and buffer:
            if not keyword_bytes or keyword_bytes in buffer:
                results.append(buffer.decode(encoding, errors="replace"))

    return results[:limit]
