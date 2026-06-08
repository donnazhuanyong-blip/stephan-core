# ChatGPT Developer Mode MCP Time Server

Minimal Python FastMCP server using the official `mcp` Python SDK and exposing one read-only tool:

- `get_current_time`

The tool returns:

- current date
- current time
- weekday
- timezone
- short period label: `morning`, `afternoon`, `evening`, or `night`

Default timezone: `Australia/Sydney`.

## Requirements

- Python 3.10 or newer
- Windows PowerShell

No OAuth, database, or write actions are used.

## Run On Windows PowerShell

This machine currently has Python installed at:

```text
C:\Users\Lenovo\AppData\Local\Programs\Python\Python312\python.exe
```

From this folder:

```powershell
cd C:\Users\Lenovo\chatgpt-devmode-mcp
C:\Users\Lenovo\AppData\Local\Programs\Python\Python312\python.exe -m pip install --upgrade -r requirements.txt
C:\Users\Lenovo\AppData\Local\Programs\Python\Python312\python.exe -u .\server.py
```

Expected console output:

```text
Time MCP running at http://localhost:8000/mcp
INFO:     Started server process ...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

The MCP server starts on:

```text
http://localhost:8000/mcp
```

Use that Streamable HTTP endpoint when configuring ChatGPT Developer Mode.

## Tool

### `get_current_time`

Optional argument:

- `timezone`: IANA timezone name, defaults to `Australia/Sydney`

Example response:

```json
{
  "date": "2026-06-08",
  "time": "23:10:30",
  "weekday": "Monday",
  "timezone": "Australia/Sydney",
  "period": "night"
}
```
