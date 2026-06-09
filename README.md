# ChatGPT Developer Mode MCP Time Server

Minimal Python FastMCP server using the official `mcp` Python SDK and exposing two read-only tools:

- `get_current_time`
- `get_conversation_context`

The tools return:

- current date
- current time
- weekday
- timezone
- short period label: `morning`, `afternoon`, `evening`, or `night`
- compact timing signals from `get_conversation_context`

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

## Render

The server binds to `0.0.0.0` and uses Render's `PORT` environment variable when present. Locally it defaults to port `8000`.

Render start command:

```bash
python -u server.py
```

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

### `get_conversation_context`

No arguments. Timezone is fixed to `Australia/Sydney`.

Use this tool only when Donna's message clearly depends on local time, daily routine, sleep, meals, eye strain, study schedule, weather, or date context. Do not use it for simple affection, jokes, short emotional replies, or casual messages unless Donna mentions tiredness, sleep, eyes, meals, study, morning/night, or asks about time/date.

Returns:

- `current_time`
- `period`
- `is_late_night`
- `is_meal_time`
- `is_sleep_time`
- `eye_rest_needed`
- `response_hint`
