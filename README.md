# ChatGPT Developer Mode MCP Time Server

Minimal Python FastMCP server using the official `mcp` Python SDK and exposing two read-only tools:

- `get_current_time`
- `get_donna_context`

The tools return:

- current date
- current time
- weekday
- timezone
- short period label: `morning`, `afternoon`, `evening`, or `night`
- Donna-specific sleep, meal, and eye-rest advice from `get_donna_context`

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

### `get_donna_context`

No arguments.

ChatGPT should use `get_donna_context` whenever replying to Donna in casual conversation, especially when the reply may depend on time, sleep, meals, study, eye strain, weather, or daily routine.

Example response:

```json
{
  "date": "2026-06-09",
  "time": "01:15:00",
  "weekday": "Tuesday",
  "timezone": "Australia/Sydney",
  "period": "night",
  "sleep_advice": "It is very late in Sydney. Donna should wind down and prioritize sleep now.",
  "meal_advice": "It is late. Donna should avoid a heavy meal; water or a small gentle snack is better if needed.",
  "eye_rest_advice": "Late night screen use is harder on the eyes. Donna should dim screens, reduce brightness, and take a real break if possible.",
  "preferred_name": "Donna"
}
```
