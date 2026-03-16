# Log Monitor API

A simple REST API for reading log files from a Unix-style `var/log` directory without manually logging into a server and opening files.

## Features

- Fetch log lines from a specified file under `var/log`
- Supports nested paths like `apache/log3.txt`
- Returns newest log entries first
- Supports fetching the last `n` entries
- Supports optional keyword filtering
- Prevents path traversal (`../../etc/passwd`)
- Efficient for large files by reading from the end in chunks
- Includes automated tests

## Project Structure

```text
log-monitor/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── log_reader.py
├── tests/
│   ├── test_api.py
│   └── test_log_reader.py
├── var/
│   └── log/
│       ├── log1.txt
│       ├── log2.txt
│       └── apache/
│           └── log3.txt
├── requirements.txt
├── pytest.ini
└── README.md

