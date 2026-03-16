from app.log_reader import resolve_log_path, tail_lines


def test_resolve_valid_path():
    path = resolve_log_path("log1.txt")
    assert path.name == "log1.txt"


def test_resolve_nested_path():
    path = resolve_log_path("apache/log3.txt")
    assert "apache" in str(path)


def test_tail_lines_basic():
    path = resolve_log_path("log1.txt")
    lines = tail_lines(path, limit=2)
    assert len(lines) == 2


def test_keyword_filter():
    path = resolve_log_path("apache/log3.txt")
    lines = tail_lines(path, limit=10, keyword="404")
    assert any("404" in line for line in lines)
